from fastapi import APIRouter, Depends, status
from typing import List
from app.schemas.loan_schema import LoanCreate, LoanResponse, LoanStatusUpdate, LoanMiniResponse
from app.services.loan_service import LoanService
from app.dependencies.loan_dependency import get_loan_service

router = APIRouter(prefix="/loans", tags=["Loans"])

@router.post("/", response_model=LoanResponse, status_code=status.HTTP_201_CREATED)
def submit_loan(loan_data: LoanCreate, service: LoanService = Depends(get_loan_service)):
    return service.submit_application(loan_data)

@router.get("/{loan_id}", response_model=LoanResponse)
def get_loan(loan_id: int, service: LoanService = Depends(get_loan_service)):
    return service.get_application(loan_id)

@router.get("/", response_model=List[LoanMiniResponse])
def get_all_loans(service: LoanService = Depends(get_loan_service)):
    return service.get_all_applications()

@router.put("/{loan_id}/approve", response_model=LoanStatusUpdate)
def approve_loan(loan_id: int, service: LoanService = Depends(get_loan_service)):
    updated_loan = service.approve_loan(loan_id)
    return {
        "message": "Loan approved successfully",
        "status": updated_loan.status
    }

@router.put("/{loan_id}/reject", response_model=LoanStatusUpdate)
def reject_loan(loan_id: int, service: LoanService = Depends(get_loan_service)):
    updated_loan = service.reject_loan(loan_id)
    return {
        "message": "Loan rejected",
        "status": updated_loan.status
    }
