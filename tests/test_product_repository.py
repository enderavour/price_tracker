
from decimal import Decimal

from app.repositories.product_repository import ProductRepository

def test_add_product(db_session, product_data):
    repository = ProductRepository(db_session)

    product = repository.add(product_data)
    db_session.commit()

    saved_product = repository.get_by_id(product.id)

    assert saved_product is not None
    assert saved_product.name == "Test product"
    assert saved_product.source_id == "12345"
    assert saved_product.price == Decimal("49.99")
    assert saved_product.brand == "Test brand"


def test_get_product_by_id(db_session, product_data):
    repository = ProductRepository(db_session)

    product = repository.add(product_data)
    db_session.commit()

    found_product = repository.get_by_id(product.id)

    assert found_product is not None
    assert found_product.id == product.id


def test_get_product_by_source(db_session, product_data):
    repository = ProductRepository(db_session)

    repository.add(product_data)
    db_session.commit()

    found_product = repository.get_by_source(
        source="decathlon",
        source_id="12345"
    )

    assert found_product is not None
    assert found_product.name == "Test product"


def test_get_product_by_source_not_found(db_session):
    repository = ProductRepository(db_session)

    found_product = repository.get_by_source(
        source="decathlon",
        source_id="unknown"
    )

    assert found_product is None


def test_update_product(db_session, product_data):
    repository = ProductRepository(db_session)

    product = repository.add(product_data)
    db_session.commit()

    updated_data = product_data.model_copy(
        update={
            "name": "Updated product",
            "price": Decimal("39.99"),
            "available": False
        }
    )

    repository.update(product, updated_data)
    db_session.commit()

    updated_product = repository.get_by_id(product.id)

    assert updated_product.name == "Updated product"
    assert updated_product.price == Decimal("39.99")
    assert updated_product.available is False


def test_delete_product(db_session, product_data):
    repository = ProductRepository(db_session)

    product = repository.add(product_data)
    db_session.commit()

    repository.delete(product)
    db_session.commit()

    deleted_product = repository.get_by_id(product.id)

    assert deleted_product is None
