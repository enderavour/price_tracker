from app.uow import ProductPriceUOW
from app.models import Product
from app.schemas import ProductData

class ProductService:
    def __init__(self, uow: ProductPriceUOW):
        self.uow = uow

    def process_product(self, product_data: ProductData):
        product = self.uow.product_repository.get_by_source(
            product_data.source,
            product_data.source_id
        )

        if product is None:
            product = self.uow.product_repository.add(product_data)
            self.uow.db.flush()

            self.uow.price_repository.add(
                product.id,
                product_data.price
            )
        else:
            price_changed = product.price != product_data.price

            self.uow.product_repository.update(product, product_data)

            if price_changed:
                self.uow.price_repository.add(
                    product.id,
                    product_data.price
                )

    def process_products(self, products: list[ProductData]):
        try:
            for product_data in products:
                self.process_product(product_data)

            self.uow.commit()
        except Exception:
            self.uow.rollback()
            raise
