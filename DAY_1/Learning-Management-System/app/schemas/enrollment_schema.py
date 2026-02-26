from pydantic import BaseModel
from typing import Optional

class EnrollmentBase(BaseModel):
    student_id: int
    course_id: int

class EnrollmentCreate(EnrollmentBase):
    pass

class EnrollmentResponse(EnrollmentBase):
    id: int

    class Config:
        from_attributes = True

class StudentEnrollmentResponse(BaseModel):
    course_id: int
    course_title: str
