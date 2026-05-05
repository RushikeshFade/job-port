from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.job import Job

router = APIRouter()


@router.post("/post-job")
def post_job(title: str, company: str, location: str, description: str, db: Session = Depends(get_db)):
    job = Job(
        title=title,
        company=company,
        location=location,
        description=description
    )

    db.add(job)
    db.commit()

    return {"message": "Job posted"}


@router.get("/jobs")
def get_jobs(db: Session = Depends(get_db)):
    jobs = db.query(Job).all()

    return jobs