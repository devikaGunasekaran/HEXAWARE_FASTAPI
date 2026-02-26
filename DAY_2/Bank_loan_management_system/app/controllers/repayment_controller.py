from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.repayment_schema import RepaymentCreate, RepaymentRead
from app.services.repayment_service import RepaymentService

router = APIRouter()
service = RepaymentService()


@router.post("/repayments", response_model=RepaymentRead)
def add_repayment(payload: RepaymentCreate, db: Session = Depends(get_db)):
    return service.add_repayment(db, payload.loan_application_id, payload.amount_paid, payload.payment_date)
