from pydantic import BaseModel
from typing import Optional
from enum import Enum

class ApplicationStatus(str, Enum):
    APPLIED = "applied"
    SHORTLISTED = "shortlisted"
    REJECTED = "rejected"

class ApplicationBase(BaseModel):
    user_id: int
    job_id: int
    status: ApplicationStatus = ApplicationStatus.APPLIED

class ApplicationCreate(BaseModel):
    user_id: int
    job_id: int

class ApplicationUpdate(BaseModel):
    status: ApplicationStatus

class ApplicationResponse(ApplicationBase):
    id: int

    class Config:
        from_attributes = True
