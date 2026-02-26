from fastapi import APIRouter, Depends, HTTPException
from app.schemas.student_schema import StudentCreate, StudentResponse
from app.services.student_service import StudentService
from app.dependencies.dependencies import get_student_service

router = APIRouter(prefix="/students", tags=["Students"])

@router.post("/", response_model=StudentResponse, status_code=201)
def register_student(student: StudentCreate, service: StudentService = Depends(get_student_service)):
    return service.register_student(student)

@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, service: StudentService = Depends(get_student_service)):
    student = service.get_student(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student
