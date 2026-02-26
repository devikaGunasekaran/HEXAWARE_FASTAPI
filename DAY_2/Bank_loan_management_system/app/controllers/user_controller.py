from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user_schema import UserCreate, UserRead, UserUpdate
from app.services.user_service import UserService

router = APIRouter()
service = UserService()


@router.post("", response_model=UserRead)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    return service.create_user(db, name=payload.name, email=str(payload.email), role=payload.role, password=payload.password)


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return service.get_user(db, user_id)


@router.get("", response_model=list[UserRead])
def list_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return service.list_users(db, skip, limit)


@router.put("/{user_id}", response_model=UserRead)
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    return service.update_user(db, user_id, **payload.model_dump(exclude_unset=True))


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    service.delete_user(db, user_id)
    return {"message": "User deleted"}
