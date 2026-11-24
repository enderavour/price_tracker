from decimal import Decimal

from app.repositories.price_repository import PriceHistoryRepository
from app.repositories.product_repository import ProductRepository


def test_add_price_history(db_session, product_data):
    product_repository = ProductRepository(db_session)
    history_repository = PriceHistoryRepository(db_session)

    product = product_repository.add(product_data)
    db_session.commit()

    history = history_repository.add(
        product_id=product.id,
        price=Decimal("49.99")
    )
    db_session.commit()

    assert history.id is not None
    assert history.product_id == product.id
    assert history.price == Decimal("49.99")


def test_get_price_history_by_product_id(db_session, product_data):
    product_repository = ProductRepository(db_session)
    history_repository = PriceHistoryRepository(db_session)

    product = product_repository.add(product_data)
    db_session.commit()

    history_repository.add(product.id, Decimal("49.99"))
    history_repository.add(product.id, Decimal("39.99"))
    db_session.commit()

    history = history_repository.get_by_product_id(product.id)

    assert len(history) == 2
    assert history[0].price == Decimal("49.99")
    assert history[1].price == Decimal("39.99")


def test_get_price_history_for_product_without_records(
    db_session,
    product_data
):
    product_repository = ProductRepository(db_session)
    history_repository = PriceHistoryRepository(db_session)

    product = product_repository.add(product_data)
    db_session.commit()

    history = history_repository.get_by_product_id(product.id)

    assert history == []
