from sqlalchemy.orm import Session
from repositories.asset_repo import AssetRepository
from schemas.asset_schema import AssetCreate, AssetUpdate
from fastapi import HTTPException, status

class AssetService:
    def __init__(self, db: Session):
        self.asset_repo = AssetRepository(db)

    def create_asset(self, asset_in: AssetCreate):
        if self.asset_repo.get_by_tag(asset_in.asset_tag):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Asset with tag {asset_in.asset_tag} already exists"
            )
        return self.asset_repo.create(asset_in)

    def get_asset(self, asset_id: int):
        asset = self.asset_repo.get_by_id(asset_id)
        if not asset:
            raise HTTPException(status_code=404, detail="Asset not found")
        return asset

    def update_asset(self, asset_id: int, asset_in: AssetUpdate):
        asset = self.asset_repo.update(asset_id, asset_in)
        if not asset:
            raise HTTPException(status_code=404, detail="Asset not found")
        return asset

    def list_assets(self, **kwargs):
        return self.asset_repo.list_assets(**kwargs)
