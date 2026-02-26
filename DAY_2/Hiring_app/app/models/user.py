from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from .base import Base
import enum

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    RECRUITER = "recruiter"
    CANDIDATE = "candidate"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    role = Column(String, default=UserRole.CANDIDATE) # Using String to keep it simple with the requirement description
    hashed_password = Column(String, nullable=False)

    applications = relationship("Application", back_populates="user")
    jobs = relationship("Job", back_populates="company")
