from datetime import date

from pydantic import BaseModel, ConfigDict

from app.models.repayment import PaymentStatus


class RepaymentCreate(BaseModel):
    loan_application_id: int
    amount_paid: float
    payment_date: date | None = None


class RepaymentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    loan_application_id: int
    amount_paid: float
    payment_date: date
    payment_status: PaymentStatus
