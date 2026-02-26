from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base

class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    manager_id = Column(Integer, ForeignKey("users.id", use_alter=True, name="fk_department_manager"), nullable=True)

    manager = relationship("User", primaryjoin="Department.manager_id == User.id", back_populates="managed_department")
    employees = relationship("User", primaryjoin="Department.id == User.department_id", back_populates="department")
