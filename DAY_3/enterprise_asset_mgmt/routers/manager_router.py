from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.session import get_db
from controllers.manager_controller import ManagerController
from dependencies.rbac import allow_roles

router = APIRouter(prefix="/manager", tags=["Manager"])
require_manager = allow_roles("MANAGER", "IT_ADMIN", "SUPERADMIN")

@router.get("/team-assets")
def view_team_assets(db: Session = Depends(get_db), current_user=Depends(require_manager)):
    # Assuming the manager can see assets of their own department
    if not current_user.department_id:
        return {"detail": "Manager not assigned to a department"}
    return ManagerController.view_department_assets(db, current_user.department_id)
