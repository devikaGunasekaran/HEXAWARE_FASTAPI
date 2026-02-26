from sqlalchemy.orm import Session
from models.department import Department
from schemas.department_schema import DepartmentCreate, DepartmentUpdate

class DepartmentRepository:
    def get_by_id(self, db: Session, department_id: int):
        return db.query(Department).filter(Department.id == department_id).first()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(Department).offset(skip).limit(limit).all()

    def create(self, db: Session, department: DepartmentCreate):
        db_dept = Department(name=department.name, manager_id=department.manager_id)
        db.add(db_dept)
        db.commit()
        db.refresh(db_dept)
        return db_dept

    def update(self, db: Session, department_id: int, department_update: DepartmentUpdate):
        db_dept = self.get_by_id(db, department_id)
        if not db_dept:
            return None
        
        dept_data = department_update.model_dump(exclude_unset=True)
        for key, value in dept_data.items():
            setattr(db_dept, key, value)
        
        db.commit()
        db.refresh(db_dept)
        return db_dept

    def delete(self, db: Session, department_id: int):
        db_dept = self.get_by_id(db, department_id)
        if db_dept:
            db.delete(db_dept)
            db.commit()
            return True
        return False

department_repo = DepartmentRepository()
