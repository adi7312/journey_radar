from fastapi import APIRouter
from api_gw.dto.requests import TripRequest
from api_gw.dto.responses import TripResponse


router = APIRouter()

import requests
import json

GOOGLE_API_BASE = "http://217.153.167.103:8000"
DELAY_API_BASE = "http://217.153.167.103:8010"

@router.post("/trip", response_model=TripResponse)
def get_trip(request: TripRequest) -> TripResponse:
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

    rsp = requests.post(f"{DELAY_API_BASE}/get-delay", json=e)
    if (rsp.status_code != 200):
        delay = 0
    else:
        delay = rsp.json()['delay_seconds']
    
    return TripResponse(
        distance_m=google_rsp["route"]["distance_m"],
        duration_s=google_rsp["route"]["duration_s"],
        delay_s=delay,
        travel_mode=f"{e['vehicle_type']}",
        start_location={"longitude": request.a_longitude, "latitude": request.a_latitude},
        end_location={"longitude": request.b_longitude, "latitude": request.b_latitude}
    )