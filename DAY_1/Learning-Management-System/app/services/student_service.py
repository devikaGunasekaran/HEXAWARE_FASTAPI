from app.repositories.student_repository import StudentRepository
from app.schemas.student_schema import StudentCreate

class StudentService:
    def __init__(self, student_repo: StudentRepository):
        self.student_repo = student_repo

    def register_student(self, student_data: StudentCreate):
        return self.student_repo.create(student_data)

    def get_student(self, student_id: int):
        return self.student_repo.get_by_id(student_id)
