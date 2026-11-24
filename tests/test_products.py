from decimal import Decimal

def test_get_products_empty(client):
    response = client.get("/products/")

    assert response.status_code == 200
    assert response.json() == []

    
def test_get_product_not_found(client):
    response = client.get("/products/999999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Product not found"
    }

def test_get_products(client, db_session, product_data):
    from app.repositories.product_repository import ProductRepository

    repository = ProductRepository(db_session)
    repository.add(product_data)
    db_session.commit()

    response = client.get("/products/")

    assert response.status_code == 200

    products = response.json()

    assert len(products) == 1
    assert products[0]["name"] == "Test product"
    assert products[0]["source"] == "decathlon"
    assert products[0]["price"] == "49.99"


def test_get_product_by_id(client, db_session, product_data):
    from app.repositories.product_repository import ProductRepository

    repository = ProductRepository(db_session)
    product = repository.add(product_data)
    db_session.commit()

    response = client.get(f"/products/{product.id}")

    assert response.status_code == 200
    assert response.json()["id"] == product.id
    assert response.json()["name"] == "Test product"


def test_get_product_price_history(client, db_session, product_data):
    from app.repositories.product_repository import ProductRepository
    from app.repositories.price_repository import PriceHistoryRepository

    product_repository = ProductRepository(db_session)
    history_repository = PriceHistoryRepository(db_session)

    product = product_repository.add(product_data)
    db_session.flush()

    history_repository.add(product.id, Decimal("49.99"))
    history_repository.add(product.id, Decimal("39.99"))

    db_session.commit()

    response = client.get(f"/products/{product.id}/history")

    assert response.status_code == 200

    history = response.json()

    assert len(history) == 2
    assert history[0]["price"] == "49.99"
    assert history[1]["price"] == "39.99"