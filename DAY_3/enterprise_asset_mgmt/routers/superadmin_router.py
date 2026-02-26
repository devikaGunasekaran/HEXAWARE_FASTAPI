from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.session import get_db
from controllers.superadmin_controller import SuperAdminController
from dependencies.rbac import allow_roles
from schemas.user_schema import UserCreate, UserResponse
from schemas.department_schema import DepartmentCreate, DepartmentResponse
from typing import List

router = APIRouter(prefix="/superadmin", tags=["Super Admin"])
require_superadmin = allow_roles("SUPERADMIN")

@router.post("/users", response_model=UserResponse)
def create_user(user_in: UserCreate, db: Session = Depends(get_db), current_user=Depends(require_superadmin)):
    return SuperAdminController.create_user(db, user_in)

@router.get("/users", response_model=List[UserResponse])
def list_users(db: Session = Depends(get_db), current_user=Depends(require_superadmin)):
    return SuperAdminController.list_users(db)

@router.post("/departments", response_model=DepartmentResponse)
def create_department(dept_in: DepartmentCreate, db: Session = Depends(get_db), current_user=Depends(require_superadmin)):
    return SuperAdminController.create_department(db, dept_in)
