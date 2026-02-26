import enum
from datetime import date

from sqlalchemy import Date, Enum, ForeignKey, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class PaymentStatus(str, enum.Enum):
    completed = "completed"
    pending = "pending"


class Repayment(Base):
    __tablename__ = "repayments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    loan_application_id: Mapped[int] = mapped_column(Integer, ForeignKey("loan_applications.id"), nullable=False)
    amount_paid: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    payment_date: Mapped[date] = mapped_column(Date, nullable=False)
    payment_status: Mapped[PaymentStatus] = mapped_column(
        Enum(PaymentStatus, name="payment_status"), nullable=False, default=PaymentStatus.completed
    )

    loan_application = relationship("LoanApplication", back_populates="repayments")
