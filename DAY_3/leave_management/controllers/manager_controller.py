from sqlalchemy.orm import Session
from services.leave_service import leave_service
from models.leave_request import LeaveStatus
from core.pagination import paginate

class ManagerController:
    def list_department_leaves(self, db: Session, department_id: int, page: int, size: int):
        leaves = leave_service.list_department_leaves(db, department_id)
        return paginate(leaves, page, size)

    def approve_leave(self, db: Session, leave_id: int, status: LeaveStatus, approver_id: int):
        return leave_service.update_leave(db, leave_id, status, approver_id)

manager_controller = ManagerController()
