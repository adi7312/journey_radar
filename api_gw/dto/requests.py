from typing import Optional, Dict
from pydantic import BaseModel

class TripRequest(BaseModel):
    a_longitude: float
    a_latitude: float
    b_longitude: float
    b_latitude: float

class StrTripRequest(BaseModel):
    origin: str
    destination: str


class ReportRequest(BaseModel):
    reporting_user_id: int
    description: str
    lattidude: float
    longidute: float
    route_name: str

class VerifyReportRequest(BaseModel):
    report_id: int
    verified: str

class CreateUser(BaseModel):
    name: str
    surname: str
    email: str

class VoteRequest(BaseModel):
    action: str  # "like" or "dislike"