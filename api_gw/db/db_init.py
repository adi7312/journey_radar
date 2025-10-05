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
                description="10 min delay",
                lattidude=50.068268756543645,
                longidute=19.947651357113628,
                route_name="50",
                creator_id=users[0].id,
                timestamp=1728102000
            ),
            Report(
                likes=3,
                dislikes=2,
                verified="unverified",
                description="Car crash",
                lattidude=50.06078216283356, 
                longidute=19.959806895097206,
                route_name="50",
                creator_id=users[1].id,
                timestamp=1728098400
            ),
            Report(
                likes=8,
                dislikes=0,
                verified="negative",
                description="Tusk",
                lattidude=50.05809590796945, 
                longidute=19.95907733426118,
                route_name="50",
                creator_id=users[2].id,
                timestamp=1728015600
            ),
            Report(
                likes=5,
                dislikes=4,
                verified="positive",
                description="Bus stop shelter near 5th Avenue is damaged after a storm.",
                lattidude=50.06576,
                longidute=19.95986,
                route_name="50",
                creator_id=users[0].id,
                timestamp=1727929200
            ),
        ]

        session.add_all(reports)
        session.commit()

        print("✅ Example data inserted successfully!")