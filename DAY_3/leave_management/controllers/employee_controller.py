from sqlalchemy.orm import Session
from services.leave_service import leave_service
from schemas.leave_schema import LeaveCreate
from models.user import User

class EmployeeController:
    def apply_leave(self, db: Session, current_user: User, leave: LeaveCreate):
        return leave_service.apply_leave(db, current_user.id, leave)

    def list_own_leaves(self, db: Session, current_user: User):
        return leave_service.list_own_leaves(db, current_user.id)

employee_controller = EmployeeController()
