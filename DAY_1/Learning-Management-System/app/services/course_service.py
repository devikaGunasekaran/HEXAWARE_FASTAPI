from app.repositories.course_repository import CourseRepository
from app.schemas.course_schema import CourseCreate

class CourseService:
    def __init__(self, course_repo: CourseRepository):
        self.course_repo = course_repo

    def create_course(self, course_data: CourseCreate):
        return self.course_repo.create(course_data)

    def get_course(self, course_id: int):
        return self.course_repo.get_by_id(course_id)

    def list_courses(self):
        return self.course_repo.get_all()
