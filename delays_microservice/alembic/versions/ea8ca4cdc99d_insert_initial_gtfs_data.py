"""Insert initial GTFS data

Revision ID: ea8ca4cdc99d
Revises: 263cce2c40bf
Create Date: 2025-10-04 18:47:24.310881

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import csv
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer, Enum
from models import VehicleType

# revision identifiers, used by Alembic.
revision: str = 'ea8ca4cdc99d'
down_revision: Union[str, Sequence[str], None] = '263cce2c40bf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def load_csv(file_path):
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)


def upgrade():
    # --- Insert Stops ---
    stops_table = table(
        'stops',
        column('id', String),
        column('vehicle_type', Enum(VehicleType)),
        column('name', String),
        column('longitude', String),
        column('latitude', String),
    )

    stops = load_csv('./static/stops.csv')
    op.bulk_insert(
        stops_table,
        [
            {
                'id': s['stop_id'],
                'name': s['stop_name'],
                'longitude': s['stop_lon'],
                'latitude': s['stop_lat'],
                'vehicle_type': VehicleType(s['source'])
            }
            for s in stops
        ]
    )

    # --- Insert Routes ---
    routes_table = table(
        'routes',
        column('id', String),
        column('vehicle_type', Enum(VehicleType)),
        column('route_name', String),
    )

    routes = load_csv('./static/routes.csv')
    op.bulk_insert(
        routes_table,
        [
            {
                'id': r['route_id'],
                'route_name': r['route_short_name'],
                'vehicle_type': VehicleType(r['source'])
            }
            for r in routes
        ]
    )

    # --- Insert Trips ---
    trips_table = table(
        'trips',
        column('id', String),
        column('vehicle_type', Enum(VehicleType)),
        column('route_id', String),
        column('route_vehicle_type', Enum(VehicleType)),
        column('headsign', String),
    )

    trips = load_csv('./static/trips.csv')
    op.bulk_insert(
        trips_table,
        [
            {
                'id': t['trip_id'],
                'vehicle_type': VehicleType(t['source']),
                'route_id': t['route_id'],
                'route_vehicle_type': VehicleType(t['source']),  # zakładam, że to ta sama kolumna
                'headsign': t['trip_headsign']
            }
            for t in trips
        ]
    )

    # --- Insert StopTimes ---
    stop_times_table = table(
        'stop_times',
        column('trip_id', String),
        column('trip_vehicle_type', Enum(VehicleType)),
        column('stop_id', String),
        column('stop_vehicle_type', Enum(VehicleType)),
        column('arrival_time', String),
        column('departure_time', String),
    )

    stop_times = load_csv('./static/stop_times.csv')
    op.bulk_insert(
        stop_times_table,
        [
            {
                'trip_id': st['trip_id'],
                'trip_vehicle_type': VehicleType(st['source']),
                'stop_id': st['stop_id'],
                'stop_vehicle_type': VehicleType(st['source']),
                'arrival_time': st['arrival_time'],
                'departure_time': st['departure_time'],
            }
            for st in stop_times
        ]
    )


def downgrade():
    op.execute("DELETE FROM stop_times")
    op.execute("DELETE FROM trips")
    op.execute("DELETE FROM routes")
    op.execute("DELETE FROM stops")
