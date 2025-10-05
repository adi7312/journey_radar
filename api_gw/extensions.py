from typing import Union
from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select
import uvicorn

DATABASE_URL = "postgresql://postgres:postgres@db_api_gw:5432/journey_radar_api_gw"
engine = create_engine(DATABASE_URL)

app = FastAPI()

def create_db_and_tables():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session


