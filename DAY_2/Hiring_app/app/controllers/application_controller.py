from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..schemas.application_schema import ApplicationCreate, ApplicationResponse, ApplicationUpdate
from ..services.application_service import ApplicationService
from typing import List

router = APIRouter(prefix="/applications", tags=["Applications"])

@router.post("/", response_model=ApplicationResponse)
def create_application(application: ApplicationCreate, db: Session = Depends(get_db)):
    service = ApplicationService(db)
    return service.create_application(application)

@router.get("/{application_id}", response_model=ApplicationResponse)
def get_application(application_id: int, db: Session = Depends(get_db)):
    service = ApplicationService(db)
    return service.get_application(application_id)

@router.get("/", response_model=List[ApplicationResponse])
def list_applications(
    skip: int = Query(0, ge=0), 
    limit: int = Query(100, ge=1), 
    db: Session = Depends(get_db)
):
    service = ApplicationService(db)
    return service.get_applications(skip=skip, limit=limit)

@router.get("/user/{user_id}", response_model=List[ApplicationResponse])
def get_user_applications(user_id: int, db: Session = Depends(get_db)):
    service = ApplicationService(db)
    return service.get_user_applications(user_id)

@router.put("/{application_id}", response_model=ApplicationResponse)
def update_application_status(
    application_id: int, 
    application: ApplicationUpdate, 
    db: Session = Depends(get_db)
):
    service = ApplicationService(db)
    return service.update_application_status(application_id, application)
