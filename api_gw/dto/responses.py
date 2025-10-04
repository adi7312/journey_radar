from typing import Optional, Dict
from pydantic import BaseModel

class TripResponse(BaseModel):
    distance_m: int
    duration_s: int
    travel_mode: str
    arrival_stop: str
    departure_stop: str
    arrival_time: int
    departure_time: int
    start_location: Dict[str, float]
    end_location: Dict[str, float]