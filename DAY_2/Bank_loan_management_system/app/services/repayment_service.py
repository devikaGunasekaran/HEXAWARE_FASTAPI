from datetime import date
from decimal import Decimal

from sqlalchemy.orm import Session

from app.exceptions.custom_exceptions import BusinessRuleViolation, NotFoundError
from app.models.loan_application import LoanStatus
from app.models.repayment import PaymentStatus, Repayment
from app.repositories.application_repository import ApplicationRepository
from app.repositories.repayment_repository import RepaymentRepository


class RepaymentService:
    def __init__(
        self,
        repo: RepaymentRepository | None = None,
        application_repo: ApplicationRepository | None = None,
    ):
        self.repo = repo or RepaymentRepository()
        self.application_repo = application_repo or ApplicationRepository()

    def add_repayment(self, db: Session, loan_application_id: int, amount_paid: float, payment_date: date | None) -> Repayment:
        application = self.application_repo.get_by_id(db, loan_application_id)
        if not application:
            raise NotFoundError("Loan application not found")

        if application.status in (LoanStatus.rejected, LoanStatus.closed):
            raise BusinessRuleViolation("Cannot add repayment for rejected or closed loans")

        if application.approved_amount is None:
            raise BusinessRuleViolation("Cannot add repayment before approval")

        total_paid = sum(Decimal(str(row.amount_paid)) for row in application.repayments)
        new_total = total_paid + Decimal(str(amount_paid))
        approved = Decimal(str(application.approved_amount))

        if new_total > approved:
            raise BusinessRuleViolation("Repayment exceeds outstanding balance")

        repayment = Repayment(
            loan_application_id=loan_application_id,
            amount_paid=amount_paid,
            payment_date=payment_date or date.today(),
            payment_status=PaymentStatus.completed,
        )

        try:
            created = self.repo.create(db, repayment)
            if new_total == approved:
                application.status = LoanStatus.closed
                db.flush()
            db.commit()
        except Exception:
            db.rollback()
            raise

        return created

    def list_repayments(self, db: Session, loan_application_id: int):
        return self.repo.list_by_application(db, loan_application_id)
