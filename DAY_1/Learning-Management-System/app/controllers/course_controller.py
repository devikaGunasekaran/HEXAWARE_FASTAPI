from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.schemas.course_schema import CourseCreate, CourseResponse
from app.services.course_service import CourseService
from app.dependencies.dependencies import get_course_service

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.post("/", response_model=CourseResponse, status_code=201)
def create_course(course: CourseCreate, service: CourseService = Depends(get_course_service)):
    return service.create_course(course)

@router.get("/", response_model=List[CourseResponse])
def list_courses(service: CourseService = Depends(get_course_service)):
    return service.list_courses()

@router.get("/{course_id}", response_model=CourseResponse)
def get_course(course_id: int, service: CourseService = Depends(get_course_service)):
    course = service.get_course(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course
