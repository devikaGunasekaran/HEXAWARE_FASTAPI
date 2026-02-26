from pydantic import BaseModel, ConfigDict

from app.models.loan_application import LoanStatus


class LoanApplicationCreate(BaseModel):
    user_id: int
    product_id: int
    requested_amount: float


class LoanApplicationStatusUpdate(BaseModel):
    status: LoanStatus
    processed_by: int | None = None
    approved_amount: float | None = None


class LoanApplicationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    product_id: int
    requested_amount: float
    approved_amount: float | None = None
    status: LoanStatus
    processed_by: int | None = None
