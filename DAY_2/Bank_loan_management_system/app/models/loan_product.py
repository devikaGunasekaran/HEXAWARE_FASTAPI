from sqlalchemy import Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class LoanProduct(Base):
    __tablename__ = "loan_products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    product_name: Mapped[str] = mapped_column(String, nullable=False)
    interest_rate: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    max_amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    tenure_months: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)

    loan_applications = relationship("LoanApplication", back_populates="product")
