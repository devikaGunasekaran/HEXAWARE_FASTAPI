from datetime import timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from core.config import settings
from core.security import verify_password, create_access_token, oauth2_scheme
from database.session import get_db
from repositories.user_repo import UserRepository
from jose import jwt, JWTError
from schemas.user_schema import TokenData

class AuthService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    def login(self, form_data: OAuth2PasswordRequestForm):
        user = self.user_repo.get_by_email(form_data.username)
        if not user or not verify_password(form_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email, "role": user.role},
            expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

    def register(self, user_in: any): # type hint as any to avoid circular import if needed, but schemas should be fine
        # Users registering themselves are always EMPLOYEES
        from models import UserRole # local import if needed
        from schemas.user_schema import UserCreate
        
        db_user = self.user_repo.get_by_email(user_in.email)
        if db_user:
            raise HTTPException(status_code=400, detail="User with this email already exists")
        
        # Override role to EMPLOYEE for public registration
        user_in.role = UserRole.EMPLOYEE
        return self.user_repo.create(user_in)

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    user_repo = UserRepository(db)
    user = user_repo.get_by_email(email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(current_user: any = Depends(get_current_user)):
    # Add logic here if you want to check if user is active/not disabled
    return current_user
