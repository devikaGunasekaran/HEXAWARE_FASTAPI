from fastapi import HTTPException
from app.repositories.enrollment_repository import EnrollmentRepository
from app.repositories.student_repository import StudentRepository
from app.repositories.course_repository import CourseRepository
from app.schemas.enrollment_schema import EnrollmentCreate

class EnrollmentService:
    def __init__(
        self, 
        enrollment_repo: EnrollmentRepository,
        student_repo: StudentRepository,
        course_repo: CourseRepository
    ):
        self.enrollment_repo = enrollment_repo
        self.student_repo = student_repo
        self.course_repo = course_repo

    def enroll_student(self, enrollment_data: EnrollmentCreate):
        # Validate student exists
        if not self.student_repo.get_by_id(enrollment_data.student_id):
            raise HTTPException(status_code=404, detail="Student not found")
        
        # Validate course exists
        if not self.course_repo.get_by_id(enrollment_data.course_id):
            raise HTTPException(status_code=404, detail="Course not found")

        # Prevent duplicate enrollment
        if self.enrollment_repo.exists(enrollment_data.student_id, enrollment_data.course_id):
            raise HTTPException(status_code=400, detail="Already enrolled")

        return self.enrollment_repo.create(enrollment_data)

    def get_all_enrollments(self):
        return self.enrollment_repo.get_all()

    def get_enrollments_by_student(self, student_id: int):
        if not self.student_repo.get_by_id(student_id):
            raise HTTPException(status_code=404, detail="Student not found")
        return self.enrollment_repo.get_enrollments_with_course_details(student_id)

    def get_enrollments_by_course(self, course_id: int):
        if not self.course_repo.get_by_id(course_id):
            raise HTTPException(status_code=404, detail="Course not found")
        return self.enrollment_repo.get_by_course(course_id)
