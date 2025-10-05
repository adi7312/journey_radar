from fastapi import APIRouter
from api_gw.dto.requests import TripRequest, StrTripRequest
from api_gw.dto.responses import TripResponse
from datetime import datetime, timezone

router = APIRouter()

import requests
import json

GOOGLE_API_BASE = "http://217.153.167.103:8000"
DELAY_API_BASE = "http://217.153.167.103:8010"
LLM_ENDPOINT = "http://217.153.167.103:8001"

def call_predict(timestamp, line_id, vehicle_type, lat, lon, endpoint=LLM_ENDPOINT, timeout=15):
    data = {
        "timestamp": str(timestamp),
        "line_id": str(line_id),
        "vehicle_type": str(vehicle_type),
        "lat": float(lat),
        "lon": float(lon),
    }
    r = requests.post(endpoint, json=data, timeout=timeout)
    try:
        return r.json()
    except Exception:
        return r.text

@router.post("/trip-geo", response_model=TripResponse)
def get_trip_geo(request: TripRequest) -> TripResponse:
    # Mock calculation for demonstration
    payload = {
        "origin": {"lat": request.a_latitude, "lng": request.a_longitude},
        "destination": {"lat": request.b_latitude, "lng": request.b_longitude},
    }
    google_rsp = requests.post(f"{GOOGLE_API_BASE}/transit", json=payload, timeout=30)
    google_rsp.raise_for_status()

    e  = {}
    e['line_name'] = google_rsp.json()['route']['steps'][1]['transit']['line_name']
    e['vehicle_type'] = google_rsp.json()['route']['steps'][1]['transit']['vehicle_type']
    e['headsign'] = google_rsp.json()['route']['steps'][1]['transit']['headsign']
    e['departure_stop'] = google_rsp.json()['route']['steps'][1]['transit']['departure_stop']
    e['departure_time'] = google_rsp.json()['route']['steps'][1]['transit']['departure_time']
    dt = datetime.fromtimestamp(e['departure_time'], tz=timezone.utc)
    formatted = dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    dep_lng = google_rsp.json()["route"]["steps"][1]["start_location"]["lng"]
    dep_lat = google_rsp.json()["route"]["steps"][1]["start_location"]["lat"]
    rsp = requests.post(f"{DELAY_API_BASE}/get-delay", json=e)
    if (rsp.status_code != 200):
        delay = 0
    else:
        delay = rsp.json()['delay_seconds']
    
    p_delay = call_predict(formatted,e["line_name"], e['vehicle_type'], dep_lat, dep_lng)

    return TripResponse(
        distance_m=google_rsp.json()["route"]["distance_m"],
        duration_s=google_rsp.json()["route"]["duration_s"],
        delay_s=delay,
        travel_mode=f"{e['vehicle_type']}",
        steps=google_rsp.json()['route']['steps'],
        predicted_delay_s=int(p_delay)
    )

@router.post("/trip", response_model=TripResponse)
def get_trip_geo(request: StrTripRequest) -> TripResponse:
    # Mock calculation for demonstration
    payload = {
        "origin": request.origin,
        "destination": request.destination
    }
    google_rsp = requests.post(f"{GOOGLE_API_BASE}/transit", json=payload, timeout=30)
    google_rsp.raise_for_status()

    e  = {}
    e['line_name'] = google_rsp.json()['route']['steps'][1]['transit']['line_name']
    e['vehicle_type'] = google_rsp.json()['route']['steps'][1]['transit']['vehicle_type']
    e['headsign'] = google_rsp.json()['route']['steps'][1]['transit']['headsign']
    e['departure_stop'] = google_rsp.json()['route']['steps'][1]['transit']['departure_stop']
    e['departure_time'] = google_rsp.json()['route']['steps'][1]['transit']['departure_time']
    dt = datetime.fromtimestamp(e['departure_time'], tz=timezone.utc)
    formatted = dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    dep_lng = google_rsp.json()["route"]["steps"][1]["start_location"]["lng"]
    dep_lat = google_rsp.json()["route"]["steps"][1]["start_location"]["lat"]
    rsp = requests.post(f"{DELAY_API_BASE}/get-delay", json=e)
    if (rsp.status_code != 200):
        delay = 0
    else:
        delay = rsp.json()['delay_seconds']
    
    p_delay = call_predict(formatted,e["line_name"], e['vehicle_type'], dep_lat, dep_lng)

    return TripResponse(
        distance_m=google_rsp.json()["route"]["distance_m"],
        duration_s=google_rsp.json()["route"]["duration_s"],
        delay_s=delay,
        travel_mode=f"{e['vehicle_type']}",
        steps=google_rsp.json()['route']['steps'],
        predicted_delay_s=int(p_delay)
    )