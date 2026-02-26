from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.application_schema import LoanApplicationCreate, LoanApplicationRead, LoanApplicationStatusUpdate
from app.schemas.repayment_schema import RepaymentRead
from app.services.application_service import ApplicationService
from app.services.repayment_service import RepaymentService

router = APIRouter()
application_service = ApplicationService()
repayment_service = RepaymentService()


@router.post("", response_model=LoanApplicationRead)
def apply_for_loan(payload: LoanApplicationCreate, db: Session = Depends(get_db)):
    return application_service.apply_for_loan(db, payload.user_id, payload.product_id, payload.requested_amount)


@router.get("/{application_id}", response_model=LoanApplicationRead)
def get_application(application_id: int, db: Session = Depends(get_db)):
    return application_service.get_application(db, application_id)


@router.get("", response_model=list[LoanApplicationRead])
def list_applications(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return application_service.list_applications(db, skip, limit)


@router.put("/{application_id}/status", response_model=LoanApplicationRead)
def update_status(application_id: int, payload: LoanApplicationStatusUpdate, db: Session = Depends(get_db)):
    return application_service.update_status(db, application_id, payload.status, payload.processed_by, payload.approved_amount)


@router.get("/{application_id}/repayments", response_model=list[RepaymentRead])
def list_repayments(application_id: int, db: Session = Depends(get_db)):
    return repayment_service.list_repayments(db, application_id)
