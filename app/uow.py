from app.repositories.price_repository import PriceHistoryRepository
from app.repositories.product_repository import ProductRepository
from sqlalchemy.orm import Session

class ProductPriceUOW:
    def __init__(self, db: Session):
        self.db = db
        self.price_repository = PriceHistoryRepository(self.db)
        self.product_repository = ProductRepository(self.db)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        if exc_type:
            self.rollback()
        self.db.close()

    def commit(self):
        self.db.commit()
        

    def rollback(self):
        self.db.rollback()