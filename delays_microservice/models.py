from sqlalchemy import Column, String, Integer, Enum, ForeignKeyConstraint, PrimaryKeyConstraint
from sqlalchemy.orm import declarative_base, relationship
import enum

Base = declarative_base()


class VehicleType(enum.Enum):
    T = "T"
    A = "A"
    M = "M"


class Stop(Base):
    __tablename__ = "stops"

    id = Column(String, nullable=False)
    vehicle_type = Column(Enum(VehicleType), nullable=False)
    name = Column(String, nullable=False)
    longitude = Column(String, nullable=False)
    latitude = Column(String, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint("id", "vehicle_type"),
    )

    stop_times = relationship("StopTime", back_populates="stop")


class Route(Base):
    __tablename__ = "routes"

    id = Column(String, nullable=False)
    vehicle_type = Column(Enum(VehicleType), nullable=False)
    route_name = Column(String, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint("id", "vehicle_type"),
    )

    trips = relationship("Trip", back_populates="route")


class Trip(Base):
    __tablename__ = "trips"

    id = Column(String, nullable=False)
    vehicle_type = Column(Enum(VehicleType), nullable=False)

    route_id = Column(String, nullable=False)
    route_vehicle_type = Column(Enum(VehicleType), nullable=False)

    headsign = Column(String, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint("id", "vehicle_type"),
        ForeignKeyConstraint(
            ["route_id", "route_vehicle_type"],
            ["routes.id", "routes.vehicle_type"],
        ),
    )

    route = relationship("Route", back_populates="trips")
    stop_times = relationship("StopTime", back_populates="trip")


class StopTime(Base):
    __tablename__ = "stop_times"

    id = Column(Integer, primary_key=True, autoincrement=True)

    trip_id = Column(String, nullable=False)
    trip_vehicle_type = Column(Enum(VehicleType), nullable=False)

    stop_id = Column(String, nullable=False)
    stop_vehicle_type = Column(Enum(VehicleType), nullable=False)

    arrival_time = Column(String, nullable=False)
    departure_time = Column(String, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(
            ["trip_id", "trip_vehicle_type"],
            ["trips.id", "trips.vehicle_type"],
        ),
        ForeignKeyConstraint(
            ["stop_id", "stop_vehicle_type"],
            ["stops.id", "stops.vehicle_type"],
        ),
    )

    trip = relationship("Trip", back_populates="stop_times")
    stop = relationship("Stop", back_populates="stop_times")
