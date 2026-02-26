from datetime import timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from core.security import verify_password, create_access_token, get_password_hash
from repositories.user_repo import user_repo
from schemas.user_schema import UserCreate, Token

class AuthService:
    def authenticate_user(self, db: Session, email, password):
        print(f"DEBUG: Authenticating user email: {email}")
        user = user_repo.get_by_email(db, email)
        if not user:
            print(f"DEBUG: User not found for email: {email}")
            return False
        
        is_valid = verify_password(password, user.password)
        if not is_valid:
            print(f"DEBUG: Invalid password for user: {email}")
            return False
            
        print(f"DEBUG: Authentication successful for: {email}")
        return user

    def login(self, db: Session, email, password):
        user = self.authenticate_user(db, email, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token = create_access_token(data={"sub": user.email, "role": str(user.role.value) if hasattr(user.role, 'value') else str(user.role)})
        return Token(access_token=access_token, token_type="bearer")

    def register(self, db: Session, user: UserCreate):
        db_user = user_repo.get_by_email(db, user.email)
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        return user_repo.create(db, user)

auth_service = AuthService()
