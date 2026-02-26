from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from services.auth_service import AuthService

class AuthController:
    @staticmethod
    def login(db: Session, form_data: OAuth2PasswordRequestForm):
        auth_service = AuthService(db)
        return auth_service.login(form_data)

    @staticmethod
    def register(db: Session, user_in: any):
        auth_service = AuthService(db)
        return auth_service.register(user_in)
