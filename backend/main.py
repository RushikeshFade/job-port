from fastapi import FastAPI
from database import Base, engine

from routes.auth_routes import router as auth_router
from routes.job_routes import router as job_router
from routes.application_routes import router as application_router

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routes
app.include_router(auth_router)
app.include_router(job_router)
app.include_router(application_router)


@app.get("/")
def home():
    return {"message": "Job Portal API running"}