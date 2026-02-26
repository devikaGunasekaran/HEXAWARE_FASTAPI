from sqlalchemy import Column, Integer, String, DateTime, JSON
from database.base import Base
from datetime import datetime

class AuditTrail(Base):
    __tablename__ = "audit_trails"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    action = Column(String) # CREATE, UPDATE, DELETE, LOGIN, etc.
    table_name = Column(String)
    record_id = Column(Integer)
    old_values = Column(JSON, nullable=True)
    new_values = Column(JSON, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
