from sqlalchemy.orm import Session
from services.request_service import RequestService
from services.assignment_service import AssignmentService
from schemas.request_schema import RequestCreate

class EmployeeController:
    @staticmethod
    def request_asset(db: Session, employee_id: int, request_in: RequestCreate):
        service = RequestService(db)
        return service.create_request(employee_id, request_in)

    @staticmethod
    def view_own_assets(db: Session, user_id: int):
        service = AssignmentService(db)
        return service.get_user_assets(user_id)
