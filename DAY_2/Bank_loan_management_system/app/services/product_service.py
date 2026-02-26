from sqlalchemy.orm import Session

from app.exceptions.custom_exceptions import NotFoundError
from app.models.loan_product import LoanProduct
from app.repositories.product_repository import ProductRepository


class ProductService:
    def __init__(self, repo: ProductRepository | None = None):
        self.repo = repo or ProductRepository()

    def create_product(self, db: Session, **data) -> LoanProduct:
        product = LoanProduct(**data)
        try:
            created = self.repo.create(db, product)
            db.commit()
            return created
        except Exception:
            db.rollback()
            raise

    def get_product(self, db: Session, product_id: int) -> LoanProduct:
        product = self.repo.get_by_id(db, product_id)
        if not product:
            raise NotFoundError("Loan product not found")
        return product

    def list_products(self, db: Session, skip: int, limit: int):
        return self.repo.list(db, skip, limit)

    def update_product(self, db: Session, product_id: int, **updates) -> LoanProduct:
        product = self.get_product(db, product_id)
        for key, value in updates.items():
            if value is not None:
                setattr(product, key, value)
        try:
            updated = self.repo.update(db, product)
            db.commit()
            return updated
        except Exception:
            db.rollback()
            raise

    def delete_product(self, db: Session, product_id: int) -> None:
        product = self.get_product(db, product_id)
        try:
            self.repo.delete(db, product)
            db.commit()
        except Exception:
            db.rollback()
            raise
