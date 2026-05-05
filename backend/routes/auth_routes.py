from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from auth import hash_password, verify_password, create_access_token

router = APIRouter()


@router.post("/register")
def register(name: str, email: str, password: str, role: str, db: Session = Depends(get_db)):
    user = User(
        name=name,
        email=email,
        password=hash_password(password),
        role=role
    )

    db.add(user)
    db.commit()

    return {"message": "User created"}


@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == email).first()

    if not user:
        return {"error": "User not found"}

    if not verify_password(password, user.password):
        return {"error": "Wrong password"}

    token = create_access_token({"user_id": user.id})

    return {"access_token": token}