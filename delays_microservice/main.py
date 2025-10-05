import uvicorn
from fastapi import FastAPI
from models import Base, VehicleType, Route, Trip, Stop, StopTime
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime
from pydantic import BaseModel
import requests
import gzip
from google.transit import gtfs_realtime_pb2
from google.protobuf.json_format import MessageToDict

from models import Base, VehicleType, Route, Trip, Stop, StopTime
from database import get_db

app = FastAPI()

VEHICLE_TYPE_MAP = {
    "TRAM": VehicleType.T,
    "BUS": VehicleType.A,
    "METRO": VehicleType.M,
    "HEAVY_RAIL": VehicleType.M
}


class SearchRequest(BaseModel):
    line_name: str
    vehicle_type: str
    headsign: str
    departure_stop: str
    departure_time: int  # timestamp


def fetch_trip_updates(type: str) -> dict:
    url = f"https://gtfs.ztp.krakow.pl/TripUpdates_{type}.pb"

    response = requests.get(url, timeout=30)
    response.raise_for_status()
    data = response.content

    try:
        data = gzip.decompress(data)
    except OSError:
        pass

    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(data)
    feed_dict = MessageToDict(feed)
    return feed_dict


@app.post("/get-delay")
def search_trip(req: SearchRequest, db: Session = Depends(get_db)):
    vehicle_type = VEHICLE_TYPE_MAP.get(req.vehicle_type.upper())
    if not vehicle_type:
        raise HTTPException(status_code=400, detail="Unsupported vehicle type")

    trip_updates_dict = fetch_trip_updates(vehicle_type.value)

    dep_time_str = datetime.fromtimestamp(req.departure_time).strftime("%H:%M:%S")

    stmt = (
        select(Trip)
        .join(Route, (Trip.route_id == Route.id) & (Trip.route_vehicle_type == Route.vehicle_type))
        .join(StopTime, (StopTime.trip_id == Trip.id) & (StopTime.trip_vehicle_type == Trip.vehicle_type))
        .join(Stop, (StopTime.stop_id == Stop.id) & (StopTime.stop_vehicle_type == Stop.vehicle_type))
        .where(
            Route.route_name == req.line_name,
            Trip.vehicle_type == vehicle_type,
            Trip.headsign == req.headsign,
            Stop.name == req.departure_stop,
            StopTime.departure_time == dep_time_str
        )
        .order_by(StopTime.departure_time.asc())
    )

    trip = db.execute(stmt).scalars().first()
    print(trip)
    if not trip:
        raise HTTPException(status_code=404, detail="No matching trip found")

    trip_update = None
    for entity in trip_updates_dict.get("entity", []):
        tu = entity.get("tripUpdate")
        if tu and tu.get("trip", {}).get("tripId") == trip.id:
            trip_update = tu
            break

    if not trip_update or not trip_update.get("stopTimeUpdate"):
        raise HTTPException(status_code=404, detail="Trip not found in trip updates")

    last_stop_update = trip_update["stopTimeUpdate"][0]
    stop_id = last_stop_update["stopId"]
    try:
        actual_arrival = int(last_stop_update.get("departure", last_stop_update['arrival']).get("time", None))
    except:
        raise HTTPException(status_code=404, detail="Unknown error")
    if actual_arrival is None:
        raise HTTPException(status_code=404, detail="Actual arrival time no found in trip updates")

    plan_stop_time = (
        db.query(StopTime)
        .filter(
            StopTime.trip_id == trip.id,
            StopTime.trip_vehicle_type == trip.vehicle_type,
            StopTime.stop_id == stop_id
        )
        .first()
    )

    if not plan_stop_time:
        raise HTTPException(status_code=404, detail="No plan stop time found")

    plan_dt = datetime.strptime(plan_stop_time.arrival_time, "%H:%M:%S")
    today = datetime.today()
    plan_timestamp = int(datetime(today.year, today.month, today.day,
                                  plan_dt.hour, plan_dt.minute, plan_dt.second).timestamp())

    delay_seconds = actual_arrival - plan_timestamp



    # === bartek ===

    stop_for_ml = (
    db.query(Stop)
    .filter(
        Stop.id == stop_id
    )
    .first()
    )

    VEHICLE_TYPE_MAP_REVERSE = {
    VehicleType.T: "TRAM",
    VehicleType.A: "BUS",
    VehicleType.M:  "HEAVY_RAIL"
}

    v_type = VEHICLE_TYPE_MAP_REVERSE.get(vehicle_type)

    payload = [{
        "timestamp": datetime.utcfromtimestamp(actual_arrival).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "line_id": req.line_name,
        "vehicle_type": v_type,
        "lat": float(stop_for_ml.latitude),
        "lon": float(stop_for_ml.longitude),
        "delay_sec": delay_seconds
    }]

    print(payload)


    try:
        resp = requests.post(
            "http://217.153.167.103:8001/ingest",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        resp.raise_for_status()
    except Exception as e:
        print(f"Failed to send ingest request: {e}")



    return {
        "trip_id": trip.id,
        "stop_id": stop_id,
        "planned_arrival": plan_stop_time.arrival_time,
        "actual_arrival": actual_arrival,
        "delay_seconds": delay_seconds
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8010)
