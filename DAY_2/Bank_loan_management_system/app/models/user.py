import enum

from sqlalchemy import Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class UserRole(str, enum.Enum):
    admin = "admin"
    loan_officer = "loan_officer"
    customer = "customer"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole, name="user_role"), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)

    loan_applications = relationship(
        "LoanApplication",
        back_populates="customer",
        foreign_keys="LoanApplication.user_id",
    )
    processed_applications = relationship(
        "LoanApplication",
        back_populates="loan_officer",
        foreign_keys="LoanApplication.processed_by",
    )
