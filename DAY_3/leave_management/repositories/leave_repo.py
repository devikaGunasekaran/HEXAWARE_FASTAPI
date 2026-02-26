from sqlalchemy.orm import Session
from models.leave_request import LeaveRequest, LeaveStatus
from sqlalchemy import or_, and_

class LeaveRepository:
    def get_by_id(self, db: Session, leave_id: int):
        return db.query(LeaveRequest).filter(LeaveRequest.id == leave_id).first()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(LeaveRequest).offset(skip).limit(limit).all()

    def count_all_leaves(self, db: Session):
        return db.query(LeaveRequest).count()

    def get_by_employee_id(self, db: Session, employee_id: int):
        return db.query(LeaveRequest).filter(LeaveRequest.employee_id == employee_id).all()

    def get_by_department_id(self, db: Session, department_id: int):
        from models.user import User
        return db.query(LeaveRequest).join(User, LeaveRequest.employee_id == User.id).filter(User.department_id == department_id).all()

    def check_overlap(self, db: Session, employee_id: int, start_date, end_date):
        return db.query(LeaveRequest).filter(
            LeaveRequest.employee_id == employee_id,
            LeaveRequest.status != LeaveStatus.REJECTED,
            or_(
                and_(LeaveRequest.start_date <= start_date, LeaveRequest.end_date >= start_date),
                and_(LeaveRequest.start_date <= end_date, LeaveRequest.end_date >= end_date),
                and_(LeaveRequest.start_date >= start_date, LeaveRequest.end_date <= end_date)
            )
        ).first()

    def create(self, db: Session, employee_id: int, start_date, end_date, reason):
        db_leave = LeaveRequest(
            employee_id=employee_id,
            start_date=start_date,
            end_date=end_date,
            reason=reason,
            status=LeaveStatus.PENDING
        )
        db.add(db_leave)
        db.commit()
        db.refresh(db_leave)
        return db_leave

    def update_status(self, db: Session, leave_id: int, status: LeaveStatus, approver_id: int):
        db_leave = self.get_by_id(db, leave_id)
        if not db_leave:
            return None
        
        db_leave.status = status
        db_leave.approved_by = approver_id
        db.commit()
        db.refresh(db_leave)
        return db_leave

leave_repo = LeaveRepository()
