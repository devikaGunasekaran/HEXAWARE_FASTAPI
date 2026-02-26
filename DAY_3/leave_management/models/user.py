from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum
from database.base import Base

class UserRole(str, enum.Enum):
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"
    EMPLOYEE = "EMPLOYEE"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(Enum(UserRole), default=UserRole.EMPLOYEE)
    department_id = Column(Integer, ForeignKey("departments.id", use_alter=True, name="fk_user_department"), nullable=True)

    # Simple relationship to avoid circular dependencies if needed
    department = relationship("Department", foreign_keys=[department_id], back_populates="employees")
    managed_department = relationship("Department", back_populates="manager", primaryjoin="User.id == Department.manager_id", uselist=False)
    leaves = relationship("LeaveRequest", back_populates="employee", primaryjoin="User.id == LeaveRequest.employee_id")
    approved_leaves = relationship("LeaveRequest", back_populates="approver", primaryjoin="User.id == LeaveRequest.approved_by")
