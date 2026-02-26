from app.repositories.loan_repository import LoanRepository
from app.services.loan_service import LoanService

# Single instance of repository (could also be injected per request)
_repository = LoanRepository()

def get_loan_service() -> LoanService:
    return LoanService(_repository)
