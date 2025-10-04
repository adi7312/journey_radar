from pydantic import BaseModel, EmailStr
from sqlmodel import SQLModel, Field
from typing import Optional


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    surname: str
    email: str


class Report(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    likes: int
    dislikes: int
    isValid: bool