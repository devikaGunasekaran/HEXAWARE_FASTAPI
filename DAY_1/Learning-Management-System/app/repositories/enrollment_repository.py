from app.core import db
from app.schemas.enrollment_schema import EnrollmentCreate

class EnrollmentRepository:
    def create(self, enrollment_data: EnrollmentCreate):
        new_enrollment = {
            "id": db.enrollment_id_counter,
            "student_id": enrollment_data.student_id,
            "course_id": enrollment_data.course_id
        }
        db.enrollments.append(new_enrollment)
        db.enrollment_id_counter += 1
        return new_enrollment

    def get_all(self):
        return db.enrollments

    def get_by_student(self, student_id: int):
        return [e for e in db.enrollments if e["student_id"] == student_id]

    def get_by_course(self, course_id: int):
        return [e for e in db.enrollments if e["course_id"] == course_id]

    def exists(self, student_id: int, course_id: int):
        for e in db.enrollments:
            if e["student_id"] == student_id and e["course_id"] == course_id:
                return True
        return False
        
    def get_enrollments_with_course_details(self, student_id: int):
        # Join with courses to get titles
        results = []
        for e in db.enrollments:
            if e["student_id"] == student_id:
                course = next((c for c in db.courses if c["id"] == e["course_id"]), None)
                if course:
                    results.append({
                        "course_id": course["id"],
                        "course_title": course["title"]
                    })
        return results
