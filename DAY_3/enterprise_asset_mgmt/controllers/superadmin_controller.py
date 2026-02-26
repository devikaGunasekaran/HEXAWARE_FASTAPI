from sqlalchemy.orm import Session
from repositories.user_repo import UserRepository
from repositories.department_repo import DepartmentRepository
from schemas.user_schema import UserCreate, UserUpdate
from schemas.department_schema import DepartmentCreate

class SuperAdminController:
    @staticmethod
    def create_user(db: Session, user_in: UserCreate):
        user_repo = UserRepository(db)
        return user_repo.create(user_in)

    @staticmethod
    def list_users(db: Session):
        user_repo = UserRepository(db)
        return user_repo.list_all()

    @staticmethod
    def create_department(db: Session, dept_in: DepartmentCreate):
        dept_repo = DepartmentRepository(db)
        return dept_repo.create(dept_in)
