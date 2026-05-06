from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from auth import hash_password, verify_password, create_access_token

router = APIRouter()

# Define request models
class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    role: str

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    user = User(
        name=request.name,
        email=request.email,
        password=hash_password(request.password),
        role=request.role
    )
    db.add(user)
    db.commit()
    return {"message": "User created"}

@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    
    if not user:
        return {"error": "User not found"}
    
    if not verify_password(request.password, user.password):
        return {"error": "Wrong password"}
    
    token = create_access_token({"user_id": user.id})
    return {"access_token": token}
