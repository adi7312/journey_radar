from typing import Union
from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select
from api_gw.db.models import *
from api_gw.db.db_init import *
from api_gw.extensions import *
from api_gw.user.user_controller import router as user_router
from api_gw.dispatcher.dispatcher_controller import router as dispatcher_router
from api_gw.reports.report_controller import router as report_router
from api_gw.trip.trip_controller import router as trip_router
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://217.153.167.103",
    "http://78.11.32.123:3000",
    "http://localhost:3000",
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()

@app.on_event("startup")
async def on_startup():
    # Create tables on startup
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    create_example_data()

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(user_router)
app.include_router(dispatcher_router)
app.include_router(report_router)
app.include_router(trip_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")