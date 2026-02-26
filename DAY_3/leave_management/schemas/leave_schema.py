from pydantic import BaseModel
from datetime import date
from typing import Optional
from models.leave_request import LeaveStatus

class LeaveBase(BaseModel):
    start_date: date
    end_date: date
    reason: str

class LeaveCreate(LeaveBase):
    pass

class LeaveUpdate(BaseModel):
    status: LeaveStatus
    approved_by: Optional[int] = None

class LeaveOut(LeaveBase):
    id: int
    employee_id: int
    status: LeaveStatus
    approved_by: Optional[int] = None

    class Config:
        from_attributes = True
