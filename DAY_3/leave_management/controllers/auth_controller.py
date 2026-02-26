from sqlalchemy.orm import Session
from services.auth_service import auth_service
from schemas.user_schema import UserCreate, Token
from fastapi.security import OAuth2PasswordRequestForm

class AuthController:
    def register(self, db: Session, user: UserCreate):
        return auth_service.register(db, user)

    def login(self, db: Session, form_data: OAuth2PasswordRequestForm):
        return auth_service.login(db, form_data.username, form_data.password)

auth_controller = AuthController()
