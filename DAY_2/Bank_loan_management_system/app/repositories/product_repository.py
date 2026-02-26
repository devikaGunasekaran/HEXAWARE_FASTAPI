from sqlalchemy.orm import Session

from app.models.loan_product import LoanProduct


class ProductRepository:
    def create(self, db: Session, product: LoanProduct) -> LoanProduct:
        db.add(product)
        db.flush()
        db.refresh(product)
        return product

    def get_by_id(self, db: Session, product_id: int) -> LoanProduct | None:
        return db.query(LoanProduct).filter(LoanProduct.id == product_id).first()

    def list(self, db: Session, skip: int, limit: int) -> list[LoanProduct]:
        return db.query(LoanProduct).offset(skip).limit(limit).all()

    def delete(self, db: Session, product: LoanProduct) -> None:
        db.delete(product)

    def update(self, db: Session, product: LoanProduct) -> LoanProduct:
        db.flush()
        db.refresh(product)
        return product
