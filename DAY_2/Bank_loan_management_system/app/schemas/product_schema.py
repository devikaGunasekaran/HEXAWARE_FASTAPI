from pydantic import BaseModel, ConfigDict


class LoanProductCreate(BaseModel):
    product_name: str
    interest_rate: float
    max_amount: float
    tenure_months: int
    description: str | None = None


class LoanProductUpdate(BaseModel):
    product_name: str | None = None
    interest_rate: float | None = None
    max_amount: float | None = None
    tenure_months: int | None = None
    description: str | None = None


class LoanProductRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_name: str
    interest_rate: float
    max_amount: float
    tenure_months: int
    description: str | None = None
