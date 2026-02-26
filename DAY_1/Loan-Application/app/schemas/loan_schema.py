from pydantic import BaseModel, Field
from typing import Optional, List

class LoanCreate(BaseModel):
    applicant_name: str = Field(..., example="Rahul Kumar")
    income: float = Field(..., gt=0, example=50000)
    loan_amount: float = Field(..., gt=0, example=200000)

class LoanResponse(BaseModel):
    id: int
    applicant_name: str
    income: float
    loan_amount: float
    status: str

class LoanStatusUpdate(BaseModel):
    message: str
    status: str

class LoanMiniResponse(BaseModel):
    id: int
    applicant_name: str
    loan_amount: float
    status: str
