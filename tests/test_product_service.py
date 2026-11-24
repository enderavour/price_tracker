from app.repositories.product_repository import ProductRepository
from app.repositories.price_repository import PriceHistoryRepository
from app.services.product_service import ProductService
from app.uow import ProductPriceUOW
from decimal import Decimal

def test_process_products(db_session, product_data):
    uow = ProductPriceUOW(db_session)
    service = ProductService(uow)

    product_data_2 = product_data.model_copy(
        update={
            "source_id": "67890",
            "name": "Second test product",
            "price": Decimal("79.99"),
        }
    )

    products = [product_data, product_data_2]

    service.process_products(products)

    product_repository = ProductRepository(db_session)

    saved_product_1 = product_repository.get_by_source(
        "decathlon", "12345"
    )
    saved_product_2 = product_repository.get_by_source(
        "decathlon", "67890"
    )

    assert saved_product_1 is not None
    assert saved_product_2 is not None

    price_repository = PriceHistoryRepository(db_session)

    history_1 = price_repository.get_by_product_id(saved_product_1.id)
    history_2 = price_repository.get_by_product_id(saved_product_2.id)

    assert len(history_1) == 1
    assert len(history_2) == 1

    assert history_1[0].price == product_data.price
    assert history_2[0].price == product_data_2.price

def test_process_product_same_price(db_session, product_data):
    uow = ProductPriceUOW(db_session)
    service = ProductService(uow)

    service.process_products([product_data])

    updated_data = product_data.model_copy(
        update={"available": False}
    )

    service.process_products([updated_data])

    product_repository = ProductRepository(db_session)
    saved_product = product_repository.get_by_source(
        "decathlon", "12345"
    )

    price_repository = PriceHistoryRepository(db_session)
    history = price_repository.get_by_product_id(saved_product.id)

    assert saved_product.available is False
    assert saved_product.price == Decimal("49.99")
    assert len(history) == 1