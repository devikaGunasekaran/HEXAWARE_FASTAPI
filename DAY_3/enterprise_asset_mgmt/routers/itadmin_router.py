from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database.session import get_db
from controllers.itadmin_controller import ITAdminController
from dependencies.rbac import allow_roles
from schemas.asset_schema import AssetCreate, AssetResponse
from schemas.assignment_schema import AssignmentCreate, AssignmentResponse
from typing import Optional

router = APIRouter(prefix="/itadmin", tags=["IT Admin"])
require_it_admin = allow_roles("IT_ADMIN", "SUPERADMIN")

@router.post("/assets", response_model=AssetResponse)
def create_asset(asset_in: AssetCreate, db: Session = Depends(get_db), current_user=Depends(require_it_admin)):
    return ITAdminController.create_asset(db, asset_in)

@router.get("/assets")
def list_assets(
    page: int = 1, 
    size: int = 20, 
    status: Optional[str] = None, 
    department_id: Optional[int] = None, 
    asset_tag: Optional[str] = None,
    db: Session = Depends(get_db), 
    current_user=Depends(require_it_admin)
):
    return ITAdminController.list_assets(db, page=page, size=size, status=status, department_id=department_id, asset_tag=asset_tag)

@router.post("/assignments", response_model=AssignmentResponse)
def assign_asset(assignment_in: AssignmentCreate, db: Session = Depends(get_db), current_user=Depends(require_it_admin)):
    return ITAdminController.assign_asset(db, assignment_in)

@router.post("/requests/{request_id}/approve")
def approve_request(request_id: int, asset_id: int, db: Session = Depends(get_db), current_user=Depends(require_it_admin)):
    return ITAdminController.approve_request(db, request_id, current_user.id, asset_id)

@router.post("/assignments/{assignment_id}/return")
def return_asset(assignment_id: int, condition: str, db: Session = Depends(get_db), current_user=Depends(require_it_admin)):
    return ITAdminController.return_asset(db, assignment_id, condition)
