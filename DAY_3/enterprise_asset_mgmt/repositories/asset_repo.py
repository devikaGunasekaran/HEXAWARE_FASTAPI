from sqlalchemy.orm import Session
from models.asset import Asset, AssetStatus
from schemas.asset_schema import AssetCreate, AssetUpdate
from core.pagination import paginate

class AssetRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, asset_id: int):
        return self.db.query(Asset).filter(Asset.id == asset_id).first()

    def get_by_tag(self, asset_tag: str):
        return self.db.query(Asset).filter(Asset.asset_tag == asset_tag).first()

    def create(self, asset_in: AssetCreate):
        db_asset = Asset(**asset_in.model_dump())
        self.db.add(db_asset)
        self.db.commit()
        self.db.refresh(db_asset)
        return db_asset

    def update(self, asset_id: int, asset_in: AssetUpdate):
        db_asset = self.get_by_id(asset_id)
        if not db_asset:
            return None
        
        update_data = asset_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_asset, field, value)
        
        self.db.commit()
        self.db.refresh(db_asset)
        return db_asset

    def list_assets(self, page: int = 1, size: int = 20, status: str = None, department_id: int = None, asset_tag: str = None):
        query = self.db.query(Asset)
        if status:
            query = query.filter(Asset.status == status)
        if department_id:
            query = query.filter(Asset.department_id == department_id)
        if asset_tag:
            query = query.filter(Asset.asset_tag.ilike(f"%{asset_tag}%"))
        
        return paginate(query, page, size)
