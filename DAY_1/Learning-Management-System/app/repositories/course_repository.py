from app.core import db
from app.schemas.course_schema import CourseCreate

class CourseRepository:
    def create(self, course_data: CourseCreate):
        new_course = {
            "id": db.course_id_counter,
            "title": course_data.title,
            "duration": course_data.duration
        }
        db.courses.append(new_course)
        db.course_id_counter += 1
        return new_course

    def get_by_id(self, course_id: int):
        for course in db.courses:
            if course["id"] == course_id:
                return course
        return None

    def get_all(self):
        return db.courses
