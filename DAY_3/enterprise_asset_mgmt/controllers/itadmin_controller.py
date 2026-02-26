from sqlalchemy.orm import Session
from services.asset_service import AssetService
from services.assignment_service import AssignmentService
from services.request_service import RequestService
from schemas.asset_schema import AssetCreate, AssetUpdate
from schemas.assignment_schema import AssignmentCreate

class ITAdminController:
    @staticmethod
    def create_asset(db: Session, asset_in: AssetCreate):
        service = AssetService(db)
        return service.create_asset(asset_in)

    @staticmethod
    def assign_asset(db: Session, assignment_in: AssignmentCreate):
        service = AssignmentService(db)
        return service.assign_asset(assignment_in)

    @staticmethod
    def approve_request(db: Session, request_id: int, admin_id: int, asset_id: int):
        service = RequestService(db)
        return service.approve_request(request_id, admin_id, asset_id)

    @staticmethod
    def return_asset(db: Session, assignment_id: int, condition: str):
        service = AssignmentService(db)
        return service.return_asset(assignment_id, condition)

    @staticmethod
    def list_assets(db: Session, **kwargs):
        service = AssetService(db)
        return service.list_assets(**kwargs)
