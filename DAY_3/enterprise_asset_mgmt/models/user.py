from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from database.base import Base
import enum

class UserRole(str, enum.Enum):
    SUPERADMIN = "SUPERADMIN"
    IT_ADMIN = "IT_ADMIN"
    MANAGER = "MANAGER"
    EMPLOYEE = "EMPLOYEE"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String, default=UserRole.EMPLOYEE)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    deleted_at = Column(DateTime, nullable=True)

    department = relationship("Department", back_populates="users", foreign_keys=[department_id])
    assignments = relationship("AssetAssignment", back_populates="user")
    requests = relationship("AssetRequest", back_populates="employee", foreign_keys="AssetRequest.employee_id")
