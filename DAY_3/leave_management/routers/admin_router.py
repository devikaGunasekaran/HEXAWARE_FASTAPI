from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database.session import get_db
from controllers.admin_controller import admin_controller
from schemas.user_schema import UserCreate, UserUpdate, UserOut
from schemas.department_schema import DepartmentCreate, DepartmentUpdate, DepartmentOut
from schemas.leave_schema import LeaveOut, LeaveUpdate
from dependencies.rbac import require_role
from models.user import UserRole, User

router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(require_role(UserRole.ADMIN))])

@router.get("/leaves")
def list_leaves(page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    return admin_controller.list_leaves(db, page, size)

@router.put("/leave/{leave_id}")
def update_leave(leave_id: int, leave_update: LeaveUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_role(UserRole.ADMIN))):
    return admin_controller.update_leave(db, leave_id, leave_update.status, current_user.id)

@router.post("/department", response_model=DepartmentOut)
def create_department(dept: DepartmentCreate, db: Session = Depends(get_db)):
    return admin_controller.create_department(db, dept)

@router.put("/department/{dept_id}", response_model=DepartmentOut)
def update_department(dept_id: int, dept_update: DepartmentUpdate, db: Session = Depends(get_db)):
    return admin_controller.update_department(db, dept_id, dept_update)

@router.post("/user", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return admin_controller.create_user(db, user)

@router.put("/user/{user_id}", response_model=UserOut)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    return admin_controller.update_user(db, user_id, user_update)
