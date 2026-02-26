from sqlalchemy.orm import Session

from app.models.loan_application import LoanApplication


class ApplicationRepository:
    def create(self, db: Session, application: LoanApplication) -> LoanApplication:
        db.add(application)
        db.flush()
        db.refresh(application)
        return application

    def get_by_id(self, db: Session, application_id: int) -> LoanApplication | None:
        return db.query(LoanApplication).filter(LoanApplication.id == application_id).first()

    def list(self, db: Session, skip: int, limit: int) -> list[LoanApplication]:
        return db.query(LoanApplication).offset(skip).limit(limit).all()

    def update(self, db: Session, application: LoanApplication) -> LoanApplication:
        db.flush()
        db.refresh(application)
        return application
