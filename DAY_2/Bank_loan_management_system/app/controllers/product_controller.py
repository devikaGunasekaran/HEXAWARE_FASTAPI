from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.product_schema import LoanProductCreate, LoanProductRead, LoanProductUpdate
from app.services.product_service import ProductService

router = APIRouter()
service = ProductService()


@router.post("", response_model=LoanProductRead)
def create_product(payload: LoanProductCreate, db: Session = Depends(get_db)):
    return service.create_product(db, **payload.model_dump())


@router.get("/{product_id}", response_model=LoanProductRead)
def get_product(product_id: int, db: Session = Depends(get_db)):
    return service.get_product(db, product_id)


@router.get("", response_model=list[LoanProductRead])
def list_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return service.list_products(db, skip, limit)


@router.put("/{product_id}", response_model=LoanProductRead)
def update_product(product_id: int, payload: LoanProductUpdate, db: Session = Depends(get_db)):
    return service.update_product(db, product_id, **payload.model_dump(exclude_unset=True))


@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    service.delete_product(db, product_id)
    return {"message": "Loan product deleted"}
