from sqlalchemy.orm import Session
from sqlalchemy import select
from decimal import Decimal
from app.models import PriceHistory

class PriceHistoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def add(self, product_id: int, price: Decimal) -> PriceHistory:
        history = PriceHistory(
            product_id=product_id,
            price=price
        )

        self.db.add(history)

        return history

    def get_by_product_id(
        self,
        product_id: int
    ) -> list[PriceHistory]:
        statement = (
            select(PriceHistory)
            .where(PriceHistory.product_id == product_id)
            .order_by(PriceHistory.recorded_at)
        )

        return list(self.db.scalars(statement).all())