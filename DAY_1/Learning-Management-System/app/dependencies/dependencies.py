from app.repositories.student_repository import StudentRepository
from app.repositories.course_repository import CourseRepository
from app.repositories.enrollment_repository import EnrollmentRepository
from app.services.student_service import StudentService
from app.services.course_service import CourseService
from app.services.enrollment_service import EnrollmentService

# Singletons for repositories (since we use in-memory lists)
student_repo = StudentRepository()
course_repo = CourseRepository()
enrollment_repo = EnrollmentRepository()

def get_student_service():
    return StudentService(student_repo)

def get_course_service():
    return CourseService(course_repo)

def get_enrollment_service():
    return EnrollmentService(enrollment_repo, student_repo, course_repo)
