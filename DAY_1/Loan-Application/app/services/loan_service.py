from typing import List, Optional
from fastapi import HTTPException, status
from app.repositories.loan_repository import LoanRepository
from app.models.loan_model import LoanApplication
from app.schemas.loan_schema import LoanCreate

class LoanService:
    def __init__(self, repository: LoanRepository):
        self.repository = repository

    def submit_application(self, loan_data: LoanCreate) -> LoanApplication:
        # Business Rule: Maximum eligible loan = income * 10
        max_eligibility = loan_data.income * 10
        
        status_val = "PENDING"
        if loan_data.loan_amount > max_eligibility:
            status_val = "REJECTED"

        new_loan = LoanApplication(
            id=0, # Will be set by repository
            applicant_name=loan_data.applicant_name,
            income=loan_data.income,
            loan_amount=loan_data.loan_amount,
            status=status_val
        )
        return self.repository.create(new_loan)

    def get_application(self, loan_id: int) -> LoanApplication:
        loan = self.repository.get_by_id(loan_id)
        if not loan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Loan application not found"
            )
        return loan

    def get_all_applications(self) -> List[LoanApplication]:
        return self.repository.get_all()

    def approve_loan(self, loan_id: int) -> LoanApplication:
        loan = self.get_application(loan_id)
        
        # Business Rule: Only pending applications can be approved
        if loan.status != "PENDING":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only pending loans can be approved"
            )

        # Business Rule check: Loan amount must not exceed eligibility limit
        max_eligibility = loan.income * 10
        if loan.loan_amount > max_eligibility:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Loan amount exceeds eligibility limit"
            )

        return self.repository.update_status(loan_id, "APPROVED")

    def reject_loan(self, loan_id: int) -> LoanApplication:
        loan = self.get_application(loan_id)
        
        # Business Rule: Only pending applications can be rejected
        if loan.status != "PENDING":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only pending loans can be rejected"
            )

        return self.repository.update_status(loan_id, "REJECTED")
