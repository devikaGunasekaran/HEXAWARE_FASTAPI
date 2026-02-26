from sqlalchemy.orm import Session
from models.department import Department
from schemas.department_schema import DepartmentCreate

class DepartmentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, dept_id: int):
        return self.db.query(Department).filter(Department.id == dept_id).first()

    def create(self, dept_in: DepartmentCreate):
        db_dept = Department(**dept_in.model_dump())
        self.db.add(db_dept)
        self.db.commit()
        self.db.refresh(db_dept)
        return db_dept

    def list_all(self):
        return self.db.query(Department).all()
