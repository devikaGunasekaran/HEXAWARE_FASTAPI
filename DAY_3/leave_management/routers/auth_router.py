from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database.session import get_db
from controllers.auth_controller import auth_controller
from schemas.user_schema import UserCreate, UserOut, Token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    return auth_controller.register(db, user)

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return auth_controller.login(db, form_data)
