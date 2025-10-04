from api_gw.extensions import engine
from sqlmodel import Field, Session
from api_gw.db.models import User, Report

def create_example_data():
    """Insert example Users and Reports into the database."""
    with Session(engine) as session:
        # Example users
        users = [
            User(name="Alice", surname="Johnson", email="alice@example.com", points=45),
            User(name="Bob", surname="Martinez", email="bob@example.com", points=30),
            User(name="Carla", surname="Nguyen", email="carla@example.com", points=55),
        ]

        session.add_all(users)
        session.commit()

        # Example reports (public transport issues)
        reports = [
            Report(
                likes=10,
                dislikes=2,
                verified="positive",
                description="Bus 24 was delayed for over 30 minutes due to road construction.",
                lattidude=40.7128,
                longidute=-74.0060,
                route_name="Bus 24",
                creator_id=users[0].id,
            ),
            Report(
                likes=3,
                dislikes=1,
                verified="unverified",
                description="Ticket machine at Central Station is not working.",
                lattidude=40.7135,
                longidute=-74.0090,
                route_name="Metro Line A",
                creator_id=users[1].id,
            ),
            Report(
                likes=8,
                dislikes=0,
                verified="negative",
                description="Reported train delay was resolved; trains are running on time now.",
                lattidude=40.7150,
                longidute=-74.0020,
                route_name="Train Route B",
                creator_id=users[2].id,
            ),
            Report(
                likes=5,
                dislikes=4,
                verified="positive",
                description="Bus stop shelter near 5th Avenue is damaged after a storm.",
                lattidude=40.7162,
                longidute=-74.0103,
                route_name="Bus 12",
                creator_id=users[0].id,
            ),
        ]

        session.add_all(reports)
        session.commit()

        print("✅ Example data inserted successfully!")