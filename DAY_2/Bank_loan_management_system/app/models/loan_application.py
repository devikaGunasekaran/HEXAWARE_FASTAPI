import enum

from sqlalchemy import Enum, ForeignKey, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class LoanStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    disbursed = "disbursed"
    closed = "closed"


class LoanApplication(Base):
    __tablename__ = "loan_applications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("loan_products.id"), nullable=False)
    requested_amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    approved_amount: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    status: Mapped[LoanStatus] = mapped_column(Enum(LoanStatus, name="loan_status"), nullable=False, default=LoanStatus.pending)
    processed_by: Mapped[int | None] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)

    customer = relationship("User", foreign_keys=[user_id], back_populates="loan_applications")
    loan_officer = relationship("User", foreign_keys=[processed_by], back_populates="processed_applications")
    product = relationship("LoanProduct", back_populates="loan_applications")
    repayments = relationship("Repayment", back_populates="loan_application", cascade="all, delete-orphan")
