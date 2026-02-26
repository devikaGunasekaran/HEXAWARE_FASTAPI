from sqlalchemy.orm import Session
from repositories.request_repo import RequestRepository
from services.assignment_service import AssignmentService
from schemas.request_schema import RequestCreate, RequestUpdate
from models.asset_request import RequestStatus
from schemas.assignment_schema import AssignmentCreate
from fastapi import HTTPException, status

class RequestService:
    def __init__(self, db: Session):
        self.request_repo = RequestRepository(db)
        self.assignment_service = AssignmentService(db)

    def create_request(self, employee_id: int, request_in: RequestCreate):
        return self.request_repo.create(employee_id, request_in)

    def approve_request(self, request_id: int, admin_id: int, asset_id: int):
        request = self.request_repo.get_by_id(request_id)
        if not request:
            raise HTTPException(status_code=404, detail="Request not found")
        
        if request.status != RequestStatus.PENDING:
            raise HTTPException(status_code=400, detail="Request is already processed")
        
        # 1. Update request status
        self.request_repo.update_status(request_id, RequestStatus.APPROVED, admin_id)
        
        # 2. Call assignment service to assign the asset
        assignment_in = AssignmentCreate(
            asset_id=asset_id,
            user_id=request.employee_id
        )
        return self.assignment_service.assign_asset(assignment_in)

    def list_requests(self, **kwargs):
        return self.request_repo.list_requests(**kwargs)
