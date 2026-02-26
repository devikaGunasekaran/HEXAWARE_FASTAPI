from sqlalchemy.orm import Session
from repositories.user_repo import user_repo
from schemas.user_schema import UserUpdate, UserCreate
from fastapi import HTTPException

class UserService:
    def get_user(self, db: Session, user_id: int):
        user = user_repo.get_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def list_users(self, db: Session, skip: int = 0, limit: int = 100):
        return user_repo.get_all(db, skip, limit)

    def create_user(self, db: Session, user: UserCreate):
        db_user = user_repo.get_by_email(db, user.email)
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        return user_repo.create(db, user)

    def update_user(self, db: Session, user_id: int, user_update: UserUpdate):
        user = user_repo.update(db, user_id, user_update)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def delete_user(self, db: Session, user_id: int):
        if not user_repo.delete(db, user_id):
            raise HTTPException(status_code=404, detail="User not found")
        return {"detail": "User deleted"}

user_service = UserService()
