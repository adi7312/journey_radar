from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from api_gw.db.models import User
from api_gw.dto.requests import CreateUser
from api_gw.extensions import get_session

router = APIRouter()

@router.post("/users/", response_model=User)
def register_user(user: CreateUser, session: Session = Depends(get_session)):
    db_user = session.exec(select(User).where(User.email == user.email)).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(
        name=user.name,
        surname=user.surname,
        email=user.email,
        points=0
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return user

@router.get("/users/{user_id}", response_model=User)
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user



