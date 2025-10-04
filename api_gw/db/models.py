from sqlmodel import SQLModel, Field
from typing import Optional, Dict


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    surname: str
    email: str
    points: int


class Report(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    likes: int
    dislikes: int
    verified: str # unverified, postiive, negative
    description: str
    lattidude: float
    longidute: float
    route_name: str
    creator_id: int


