from sqlalchemy.orm import Session
from ..repositories.user_repository import UserRepository
from ..schemas.user_schema import UserCreate, UserUpdate
from ..exceptions.custom_exceptions import UserNotFoundException, EmailAlreadyExistsException
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def get_user(self, user_id: int):
        user = self.repository.get_user(user_id)
        if not user:
            raise UserNotFoundException(user_id)
        return user

    def get_users(self, skip: int = 0, limit: int = 100):
        return self.repository.get_users(skip, limit)

    def create_user(self, user: UserCreate):
        if self.repository.get_user_by_email(user.email):
            raise EmailAlreadyExistsException(user.email)
        
        hashed_password = pwd_context.hash(user.password)
        return self.repository.create_user(user, hashed_password)

    def update_user(self, user_id: int, user: UserUpdate):
        self.get_user(user_id) # Check if exists
        user_data = user.dict(exclude_unset=True)
        if "password" in user_data:
            user_data["hashed_password"] = pwd_context.hash(user_data.pop("password"))
        return self.repository.update_user(user_id, user_data)

    def delete_user(self, user_id: int):
        self.get_user(user_id) # Check if exists
        return self.repository.delete_user(user_id)
