from dataclasses import dataclass

@dataclass
class LoanApplication:
    id: int
    applicant_name: str
    income: float
    loan_amount: float
    status: str # PENDING, APPROVED, REJECTED
