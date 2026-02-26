from fastapi import APIRouter, Depends
from typing import List
from app.schemas.enrollment_schema import EnrollmentCreate, EnrollmentResponse, StudentEnrollmentResponse
from app.services.enrollment_service import EnrollmentService
from app.dependencies.dependencies import get_enrollment_service

router = APIRouter(tags=["Enrollments"])

@router.post("/enrollments", response_model=EnrollmentResponse, status_code=201)
def enroll_student(enrollment: EnrollmentCreate, service: EnrollmentService = Depends(get_enrollment_service)):
    return service.enroll_student(enrollment)

@router.get("/enrollments", response_model=List[EnrollmentResponse])
def list_enrollments(service: EnrollmentService = Depends(get_enrollment_service)):
    return service.get_all_enrollments()

@router.get("/students/{student_id}/enrollments", response_model=List[StudentEnrollmentResponse])
def get_enrollments_by_student(student_id: int, service: EnrollmentService = Depends(get_enrollment_service)):
    return service.get_enrollments_by_student(student_id)

@router.get("/courses/{course_id}/enrollments", response_model=List[EnrollmentResponse])
def get_enrollments_by_course(course_id: int, service: EnrollmentService = Depends(get_enrollment_service)):
    return service.get_enrollments_by_course(course_id)
