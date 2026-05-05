from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.application import Application

router = APIRouter()


@router.post("/apply")
def apply(job_id: int, user_id: int, resume: str, db: Session = Depends(get_db)):

    app = Application(
        job_id=job_id,
        user_id=user_id,
        resume=resume
    )

    db.add(app)
    db.commit()

    return {"message": "Application submitted"}