from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from models.asset_request import RequestStatus

class RequestBase(BaseModel):
    asset_type: str
    reason: str

class RequestCreate(RequestBase):
    pass

class RequestUpdate(BaseModel):
    status: RequestStatus
    asset_id: Optional[int] = None # When approving, we might want to specify which asset

class RequestResponse(RequestBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    employee_id: int
    status: RequestStatus
    approved_by: Optional[int] = None
    created_at: datetime
