from typing import Optional, Dict
from pydantic import BaseModel

class TripResponse(BaseModel):
    distance_m: int
    duration_s: int
    delay_s: int
    travel_mode: str
    start_location: Dict[str, float]
    end_location: Dict[str, float]