from sqlalchemy.orm import Session
from repositories.department_repo import department_repo
from schemas.department_schema import DepartmentCreate, DepartmentUpdate
from fastapi import HTTPException

class DepartmentService:
    def get_department(self, db: Session, dept_id: int):
        dept = department_repo.get_by_id(db, dept_id)
        if not dept:
            raise HTTPException(status_code=404, detail="Department not found")
        return dept

    def list_departments(self, db: Session, skip: int = 0, limit: int = 100):
        return department_repo.get_all(db, skip, limit)

    def create_department(self, db: Session, department: DepartmentCreate):
        return department_repo.create(db, department)

    def update_department(self, db: Session, dept_id: int, department_update: DepartmentUpdate):
        dept = department_repo.update(db, dept_id, department_update)
        if not dept:
            raise HTTPException(status_code=404, detail="Department not found")
        return dept

    def delete_department(self, db: Session, dept_id: int):
        if not department_repo.delete(db, dept_id):
            raise HTTPException(status_code=404, detail="Department not found")
        return {"detail": "Department deleted"}

department_service = DepartmentService()
