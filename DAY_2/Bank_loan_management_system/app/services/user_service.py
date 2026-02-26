import hashlib

from sqlalchemy.orm import Session

from app.exceptions.custom_exceptions import BusinessRuleViolation, NotFoundError
from app.models.user import User
from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, repo: UserRepository | None = None):
        self.repo = repo or UserRepository()

    @staticmethod
    def _hash_password(password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def create_user(self, db: Session, name: str, email: str, role, password: str) -> User:
        if self.repo.get_by_email(db, email):
            raise BusinessRuleViolation("Email already exists")

        user = User(name=name, email=email, role=role, hashed_password=self._hash_password(password))
        try:
            created = self.repo.create(db, user)
            db.commit()
            return created
        except Exception:
            db.rollback()
            raise

    def get_user(self, db: Session, user_id: int) -> User:
        user = self.repo.get_by_id(db, user_id)
        if not user:
            raise NotFoundError("User not found")
        return user

    def list_users(self, db: Session, skip: int, limit: int):
        return self.repo.list(db, skip, limit)

    def update_user(self, db: Session, user_id: int, **updates) -> User:
        user = self.get_user(db, user_id)

        if updates.get("email"):
            existing = self.repo.get_by_email(db, updates["email"])
            if existing and existing.id != user.id:
                raise BusinessRuleViolation("Email already exists")

        if updates.get("password"):
            updates["hashed_password"] = self._hash_password(updates.pop("password"))

        for key, value in updates.items():
            if value is not None:
                setattr(user, key, value)

        try:
            updated = self.repo.update(db, user)
            db.commit()
            return updated
        except Exception:
            db.rollback()
            raise

    def delete_user(self, db: Session, user_id: int) -> None:
        user = self.get_user(db, user_id)
        try:
            self.repo.delete(db, user)
            db.commit()
        except Exception:
            db.rollback()
            raise
