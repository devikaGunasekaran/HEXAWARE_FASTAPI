from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    salary = Column(Float, nullable=True)
    company_id = Column(Integer, ForeignKey("users.id"))

    company = relationship("User", back_populates="jobs")
    applications = relationship("Application", back_populates="job")
