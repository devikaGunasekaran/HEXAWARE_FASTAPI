from sqlalchemy.orm import Session
from services.user_service import user_service
from services.department_service import department_service
from services.leave_service import leave_service
from schemas.user_schema import UserCreate, UserUpdate
from schemas.department_schema import DepartmentCreate, DepartmentUpdate
from models.leave_request import LeaveStatus
from core.pagination import paginate

class AdminController:
    def list_leaves(self, db: Session, page: int, size: int):
        leaves = leave_service.list_all_leaves(db, skip=(page-1)*size, limit=size)
        total_count = leave_service.count_leaves(db)
        return paginate(leaves, page, size)

    def update_leave(self, db: Session, leave_id: int, status: LeaveStatus, approver_id: int):
        return leave_service.admin_override(db, leave_id, status, approver_id)

    def create_department(self, db: Session, department: DepartmentCreate):
        return department_service.create_department(db, department)

    def update_department(self, db: Session, dept_id: int, department_update: DepartmentUpdate):
        return department_service.update_department(db, dept_id, department_update)

    def create_user(self, db: Session, user: UserCreate):
        return user_service.create_user(db, user)

    def update_user(self, db: Session, user_id: int, user_update: UserUpdate):
        return user_service.update_user(db, user_id, user_update)

admin_controller = AdminController()
