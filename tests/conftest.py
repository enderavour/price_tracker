import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.schemas import ProductData
from app.routers.products import get_db
from fastapi.testclient import TestClient
from app.models import Product, PriceHistory
from app.main import app
from sqlalchemy.pool import StaticPool

@pytest.fixture
def db_session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )

    TestingSessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False
    )

    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    yield db

    db.close()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()

@pytest.fixture
def product_data():
    return ProductData(
        source_id="12345",
        source="decathlon",
        name="Test product",
        brand="Test brand",
        price="49.99",
        regular_price="59.99",
        currency="EUR",
        category="test",
        url="https://example.com/product",
        image_url="https://example.com/image.jpg",
        available=True
    )

@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()