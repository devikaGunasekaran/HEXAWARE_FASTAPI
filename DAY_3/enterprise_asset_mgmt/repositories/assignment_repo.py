from sqlalchemy.orm import Session
from models.asset_assignment import AssetAssignment
from schemas.assignment_schema import AssignmentCreate
from datetime import datetime

class AssignmentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, assignment_id: int):
        return self.db.query(AssetAssignment).filter(AssetAssignment.id == assignment_id).first()

    def get_active_by_asset(self, asset_id: int):
        return self.db.query(AssetAssignment).filter(
            AssetAssignment.asset_id == asset_id,
            AssetAssignment.returned_date == None
        ).first()

    def create(self, assignment_in: AssignmentCreate):
        db_assignment = AssetAssignment(**assignment_in.model_dump())
        self.db.add(db_assignment)
        self.db.commit()
        self.db.refresh(db_assignment)
        return db_assignment

    def mark_returned(self, assignment_id: int, condition: str):
        db_assignment = self.get_by_id(assignment_id)
        if db_assignment:
            db_assignment.returned_date = datetime.utcnow()
            db_assignment.condition_on_return = condition
            self.db.commit()
            self.db.refresh(db_assignment)
            return db_assignment
        return None

    def list_by_user(self, user_id: int):
        return self.db.query(AssetAssignment).filter(AssetAssignment.user_id == user_id).all()
