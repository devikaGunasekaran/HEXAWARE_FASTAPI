from sqlalchemy.orm import Session
from models.asset_request import AssetRequest, RequestStatus
from schemas.request_schema import RequestCreate
from core.pagination import paginate

class RequestRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, request_id: int):
        return self.db.query(AssetRequest).filter(AssetRequest.id == request_id).first()

    def create(self, employee_id: int, request_in: RequestCreate):
        db_request = AssetRequest(
            employee_id=employee_id,
            **request_in.model_dump()
        )
        self.db.add(db_request)
        self.db.commit()
        self.db.refresh(db_request)
        return db_request

    def update_status(self, request_id: int, status: RequestStatus, approved_by: int = None):
        db_request = self.get_by_id(request_id)
        if db_request:
            db_request.status = status
            if approved_by:
                db_request.approved_by = approved_by
            self.db.commit()
            self.db.refresh(db_request)
            return db_request
        return None

    def list_requests(self, page: int = 1, size: int = 20, employee_id: int = None, status: str = None):
        query = self.db.query(AssetRequest)
        if employee_id:
            query = query.filter(AssetRequest.employee_id == employee_id)
        if status:
            query = query.filter(AssetRequest.status == status)
        
        return paginate(query, page, size)
