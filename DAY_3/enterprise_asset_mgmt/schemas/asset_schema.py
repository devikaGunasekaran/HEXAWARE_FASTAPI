from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date
from models.asset import AssetStatus

class AssetBase(BaseModel):
    asset_tag: str
    asset_type: str
    brand: str
    model: str
    purchase_date: date
    status: AssetStatus = AssetStatus.AVAILABLE
    department_id: Optional[int] = None

class AssetCreate(AssetBase):
    pass

class AssetUpdate(BaseModel):
    asset_tag: Optional[str] = None
    asset_type: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    purchase_date: Optional[date] = None
    status: Optional[AssetStatus] = None
    department_id: Optional[int] = None

class AssetResponse(AssetBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
