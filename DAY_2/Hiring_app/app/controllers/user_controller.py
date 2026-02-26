from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..schemas.user_schema import UserCreate, UserResponse, UserUpdate
from ..services.user_service import UserService
from typing import List

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.create_user(user)

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.get_user(user_id)

@router.get("/", response_model=List[UserResponse])
def list_users(
    skip: int = Query(0, ge=0), 
    limit: int = Query(100, ge=1), 
    db: Session = Depends(get_db)
):
    service = UserService(db)
    return service.get_users(skip=skip, limit=limit)

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.update_user(user_id, user)

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    service = UserService(db)
    service.delete_user(user_id)
    return {"message": "User deleted successfully"}
