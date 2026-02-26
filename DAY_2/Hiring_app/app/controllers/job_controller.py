from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..schemas.job_schema import JobCreate, JobResponse, JobUpdate
from ..services.job_service import JobService
from typing import List

router = APIRouter(prefix="/jobs", tags=["Jobs"])

@router.post("/", response_model=JobResponse)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    service = JobService(db)
    return service.create_job(job)

@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    service = JobService(db)
    return service.get_job(job_id)

@router.get("/", response_model=List[JobResponse])
def list_jobs(
    skip: int = Query(0, ge=0), 
    limit: int = Query(10, ge=1), 
    db: Session = Depends(get_db)
):
    service = JobService(db)
    return service.get_jobs(skip=skip, limit=limit)

@router.put("/{job_id}", response_model=JobResponse)
def update_job(job_id: int, job: JobUpdate, db: Session = Depends(get_db)):
    service = JobService(db)
    return service.update_job(job_id, job)

@router.delete("/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db)):
    service = JobService(db)
    service.delete_job(job_id)
    return {"message": "Job deleted successfully"}
