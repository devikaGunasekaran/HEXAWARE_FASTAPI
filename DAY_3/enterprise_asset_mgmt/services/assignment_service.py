from sqlalchemy.orm import Session
from repositories.assignment_repo import AssignmentRepository
from repositories.asset_repo import AssetRepository
from schemas.assignment_schema import AssignmentCreate
from models.asset import AssetStatus
from fastapi import HTTPException, status
from schemas.asset_schema import AssetUpdate

class AssignmentService:
    def __init__(self, db: Session):
        self.assignment_repo = AssignmentRepository(db)
        self.asset_repo = AssetRepository(db)

    def assign_asset(self, assignment_in: AssignmentCreate):
        asset = self.asset_repo.get_by_id(assignment_in.asset_id)
        if not asset:
            raise HTTPException(status_code=404, detail="Asset not found")
        
        if asset.status != AssetStatus.AVAILABLE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Asset is not available for assignment. Current status: {asset.status}"
            )
        
        # Create assignment
        assignment = self.assignment_repo.create(assignment_in)
        
        # Update asset status
        self.asset_repo.update(asset.id, AssetUpdate(status=AssetStatus.ASSIGNED))
        
        return assignment

    def return_asset(self, assignment_id: int, condition: str):
        assignment = self.assignment_repo.get_by_id(assignment_id)
        if not assignment or assignment.returned_date:
            raise HTTPException(status_code=400, detail="Invalid assignment or already returned")
        
        # Mark as returned
        returned_assignment = self.assignment_repo.mark_returned(assignment_id, condition)
        
        # Update asset status back to AVAILABLE
        self.asset_repo.update(assignment.asset_id, AssetUpdate(status=AssetStatus.AVAILABLE))
        
        return returned_assignment

    def get_user_assets(self, user_id: int):
        return self.assignment_repo.list_by_user(user_id)
