from typing import Union
from fastapi import FastAPI
from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/journey_radar_api_gw"

engine = create_engine(DATABASE_URL)

app = FastAPI()

# Create tables if they don't exist
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id,