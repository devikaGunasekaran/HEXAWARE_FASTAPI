import logging
from decimal import Decimal

from sqlalchemy.orm import Session

from app.exceptions.custom_exceptions import BusinessRuleViolation, NotFoundError, UnauthorizedOperation
from app.models.loan_application import LoanApplication, LoanStatus
from app.models.user import UserRole
from app.repositories.application_repository import ApplicationRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.user_repository import UserRepository

logger = logging.getLogger(__name__)


class ApplicationService:
    def __init__(
        self,
        repo: ApplicationRepository | None = None,
        product_repo: ProductRepository | None = None,
        user_repo: UserRepository | None = None,
    ):
        self.repo = repo or ApplicationRepository()
        self.product_repo = product_repo or ProductRepository()
        self.user_repo = user_repo or UserRepository()

    def apply_for_loan(self, db: Session, user_id: int, product_id: int, requested_amount: float) -> LoanApplication:
        user = self.user_repo.get_by_id(db, user_id)
        if not user:
            raise NotFoundError("User not found")

        product = self.product_repo.get_by_id(db, product_id)
        if not product:
            raise NotFoundError("Loan product not found")

        if Decimal(str(requested_amount)) > Decimal(str(product.max_amount)):
            raise BusinessRuleViolation("Requested amount exceeds product maximum")

        application = LoanApplication(
            user_id=user_id,
            product_id=product_id,
            requested_amount=requested_amount,
            status=LoanStatus.pending,
        )

        try:
            created = self.repo.create(db, application)
            db.commit()
            return created
        except Exception:
            db.rollback()
            raise

    def get_application(self, db: Session, application_id: int) -> LoanApplication:
        application = self.repo.get_by_id(db, application_id)
        if not application:
            raise NotFoundError("Loan application not found")
        return application

    def list_applications(self, db: Session, skip: int, limit: int):
        return self.repo.list(db, skip, limit)

    def update_status(
        self,
        db: Session,
        application_id: int,
        status: LoanStatus,
        processed_by: int | None,
        approved_amount: float | None,
    ) -> LoanApplication:
        application = self.get_application(db, application_id)

        if status in (LoanStatus.approved, LoanStatus.rejected, LoanStatus.disbursed):
            if not processed_by:
                raise BusinessRuleViolation("processed_by is required for this status")
            officer = self.user_repo.get_by_id(db, processed_by)
            if not officer:
                raise NotFoundError("Processing user not found")
            if officer.role != UserRole.loan_officer:
                raise UnauthorizedOperation("Only loan officers can approve/reject/disburse")
            application.processed_by = processed_by

        if status == LoanStatus.approved:
            if approved_amount is None:
                raise BusinessRuleViolation("approved_amount is required for approval")
            product = self.product_repo.get_by_id(db, application.product_id)
            if not product:
                raise NotFoundError("Loan product not found")
            if Decimal(str(approved_amount)) > Decimal(str(product.max_amount)):
                raise BusinessRuleViolation("Approved amount exceeds product maximum")
            application.approved_amount = approved_amount

        if status == LoanStatus.disbursed and application.status != LoanStatus.approved:
            raise BusinessRuleViolation("Cannot disburse unless status is approved")

        if status == LoanStatus.closed:
            raise BusinessRuleViolation("Loan closes only after full repayment")

        application.status = status

        try:
            updated = self.repo.update(db, application)
            db.commit()
        except Exception:
            db.rollback()
            raise

        if status in (LoanStatus.approved, LoanStatus.rejected):
            logger.info("Audit: application_id=%s status=%s processed_by=%s", application_id, status.value, processed_by)

        return updated
