from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class AssignmentBase(BaseModel):
    asset_id: int
    user_id: int

class AssignmentCreate(AssignmentBase):
    pass

class AssignmentReturn(BaseModel):
    condition_on_return: str

class AssignmentResponse(AssignmentBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    assigned_date: datetime
    returned_date: Optional[datetime] = None
    condition_on_return: Optional[str] = None
