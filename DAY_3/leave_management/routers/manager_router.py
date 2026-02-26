from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database.session import get_db
from controllers.manager_controller import manager_controller
from schemas.leave_schema import LeaveUpdate
from dependencies.rbac import require_role
from models.user import UserRole, User

router = APIRouter(prefix="/manager", tags=["manager"], dependencies=[Depends(require_role(UserRole.MANAGER))])

@router.get("/department-leaves")
def list_dept_leaves(page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=100), db: Session = Depends(get_db), current_user: User = Depends(require_role(UserRole.MANAGER))):
    if not current_user.department_id:
        return {"detail": "Manager not assigned to a department"}
    return manager_controller.list_department_leaves(db, current_user.department_id, page, size)

@router.put("/leave/{leave_id}")
def approve_leave(leave_id: int, leave_update: LeaveUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_role(UserRole.MANAGER))):
    return manager_controller.approve_leave(db, leave_id, leave_update.status, current_user.id)
