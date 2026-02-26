from app.core import db
from app.schemas.student_schema import StudentCreate

class StudentRepository:
    def create(self, student_data: StudentCreate):
        new_student = {
            "id": db.student_id_counter,
            "name": student_data.name,
            "email": student_data.email
        }
        db.students.append(new_student)
        db.student_id_counter += 1
        return new_student

    def get_by_id(self, student_id: int):
        for student in db.students:
            if student["id"] == student_id:
                return student
        return None

    def get_all(self):
        return db.students
