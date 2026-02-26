from sqlalchemy.orm import Session
from services.asset_service import AssetService
from models.user import User

class ManagerController:
    @staticmethod
    def view_department_assets(db: Session, department_id: int):
        service = AssetService(db)
        return service.list_assets(department_id=department_id)
