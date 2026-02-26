from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.session import get_db
from controllers.employee_controller import EmployeeController
from dependencies.rbac import allow_roles
from schemas.request_schema import RequestCreate, RequestResponse
from schemas.assignment_schema import AssignmentResponse
from typing import List

router = APIRouter(prefix="/employee", tags=["Employee"])
require_employee = allow_roles("EMPLOYEE", "MANAGER", "IT_ADMIN", "SUPERADMIN")

@router.post("/requests", response_model=RequestResponse)
def request_asset(request_in: RequestCreate, db: Session = Depends(get_db), current_user=Depends(require_employee)):
    return EmployeeController.request_asset(db, current_user.id, request_in)

@router.get("/my-assets", response_model=List[AssignmentResponse])
def view_my_assets(db: Session = Depends(get_db), current_user=Depends(require_employee)):
    return EmployeeController.view_own_assets(db, current_user.id)
