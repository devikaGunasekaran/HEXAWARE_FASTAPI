from sqlalchemy.orm import Session
from repositories.leave_repo import leave_repo
from schemas.leave_schema import LeaveCreate, LeaveUpdate
from models.leave_request import LeaveStatus
from fastapi import HTTPException
from datetime import date

class LeaveService:
    def list_all_leaves(self, db: Session, skip: int = 0, limit: int = 100):
        return leave_repo.get_all(db, skip, limit)

    def count_leaves(self, db: Session):
        return leave_repo.count_all_leaves(db)

    def list_own_leaves(self, db: Session, employee_id: int):
        return leave_repo.get_by_employee_id(db, employee_id)

    def list_department_leaves(self, db: Session, department_id: int):
        return leave_repo.get_by_department_id(db, department_id)

    def apply_leave(self, db: Session, employee_id: int, leave: LeaveCreate):
        if leave.start_date < date.today():
            raise HTTPException(status_code=400, detail="Start date cannot be in the past")
        
        if leave.end_date < leave.start_date:
            raise HTTPException(status_code=400, detail="End date must be after start date")
        
        overlap_leave = leave_repo.check_overlap(db, employee_id, leave.start_date, leave.end_date)
        if overlap_leave:
            raise HTTPException(status_code=400, detail="Another leave overlaps with these dates")
        
        return leave_repo.create(db, employee_id, leave.start_date, leave.end_date, leave.reason)

    def update_leave(self, db: Session, leave_id: int, status: LeaveStatus, approver_id: int):
        leave = leave_repo.get_by_id(db, leave_id)
        if not leave:
            raise HTTPException(status_code=404, detail="Leave request not found")
        
        if leave.status != LeaveStatus.PENDING:
            raise HTTPException(status_code=400, detail=f"Leave request already {leave.status}")
        
        return leave_repo.update_status(db, leave_id, status, approver_id)

    def admin_override(self, db: Session, leave_id: int, status: LeaveStatus, approver_id: int):
        leave = leave_repo.get_by_id(db, leave_id)
        if not leave:
            raise HTTPException(status_code=404, detail="Leave request not found")
        
        return leave_repo.update_status(db, leave_id, status, approver_id)

leave_service = LeaveService()
