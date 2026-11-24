
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Product
from app.schemas import ProductData


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def add(self, product_data: ProductData) -> Product:
        product = Product(
            source=product_data.source,
            source_id=product_data.source_id,
            name=product_data.name,
            brand=product_data.brand,
            price=product_data.price,
            regular_price=product_data.regular_price,
            currency=product_data.currency,
            category=product_data.category,
            url=str(product_data.url),
            image_url=str(product_data.image_url) if product_data.image_url else None,
            available=product_data.available,
        )

        self.db.add(product)
        return product

    def get_by_id(self, product_id: int) -> Product | None:
        return self.db.get(Product, product_id)

    def get_by_source(
        self,
        source: str,
        source_id: str
    ) -> Product | None:
        statement = select(Product).where(
            Product.source == source,
            Product.source_id == source_id
        )
        return self.db.scalar(statement)

    def get_all(self, limit: int = 100, offset: int = 0) -> list[Product]:
        statement = (
            select(Product)
            .order_by(Product.id)
            .limit(limit)
            .offset(offset)
        )

        return list(self.db.scalars(statement).all())

    def update(
        self,
        product: Product,
        product_data: ProductData
    ) -> Product:
        product.name = product_data.name
        product.brand = product_data.brand
        product.price = product_data.price
        product.regular_price = product_data.regular_price
        product.currency = product_data.currency
        product.category = product_data.category
        product.url = str(product_data.url)
        product.image_url = str(product_data.image_url) if product_data.image_url else None
        product.available = product_data.available

        return product

    def delete(self, product: Product) -> None:
        self.db.delete(product)
