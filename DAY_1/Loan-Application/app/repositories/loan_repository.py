from typing import List, Optional
from app.models.loan_model import LoanApplication

# In-memory storage
loans_db: List[LoanApplication] = []
current_id = 1

class LoanRepository:
    def create(self, loan: LoanApplication) -> LoanApplication:
        global current_id
        loan.id = current_id
        loans_db.append(loan)
        current_id += 1
        return loan

    def get_all(self) -> List[LoanApplication]:
        return loans_db

    def get_by_id(self, loan_id: int) -> Optional[LoanApplication]:
        for loan in loans_db:
            if loan.id == loan_id:
                return loan
        return None

    def update_status(self, loan_id: int, status: str) -> Optional[LoanApplication]:
        loan = self.get_by_id(loan_id)
        if loan:
            loan.status = status
            return loan
        return None
