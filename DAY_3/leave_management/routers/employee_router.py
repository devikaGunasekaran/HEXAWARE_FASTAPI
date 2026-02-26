from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.session import get_db
from controllers.employee_controller import employee_controller
from schemas.leave_schema import LeaveCreate, LeaveOut
from dependencies.rbac import get_current_user, require_role
from models.user import UserRole, User
from typing import List

router = APIRouter(prefix="/employee", tags=["employee"], dependencies=[Depends(require_role(UserRole.EMPLOYEE))])

@router.post("/apply-leave", response_model=LeaveOut)
def apply_leave(leave: LeaveCreate, db: Session = Depends(get_db), current_user: User = Depends(require_role(UserRole.EMPLOYEE))):
    return employee_controller.apply_leave(db, current_user, leave)

@router.get("/my-leaves", response_model=List[LeaveOut])
def list_my_leaves(db: Session = Depends(get_db), current_user: User = Depends(require_role(UserRole.EMPLOYEE))):
    return employee_controller.list_own_leaves(db, current_user)
