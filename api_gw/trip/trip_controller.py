from fastapi import APIRouter
from api_gw.dto.requests import TripRequest
from api_gw.dto.responses import TripResponse


router = APIRouter()

@router.post("/trip", response_model=TripResponse)
def get_trip(request: TripRequest) -> TripResponse:
    # Mock calculation for demonstration
    distance = ((request.a_longitude - request.b_longitude) ** 2 + (request.a_latitude - request.b_latitude) ** 2) ** 0.5 * 111_000  # meters
    duration = int(distance / 1.4)  # assuming walking speed ~1.4 m/s

    return TripResponse(
        distance_m=int(distance),
        duration_s=duration,
        travel_mode="walking",
        arrival_stop="Destination",
        departure_stop="Origin",
        arrival_time=1633035600 + duration,  # mock timestamp
        departure_time=1633035600,           # mock timestamp
        start_location={"longitude": request.a_longitude, "latitude": request.a_latitude},
        end_location={"longitude": request.b_longitude, "latitude": request.b_latitude}
    )