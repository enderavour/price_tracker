import pytest
from app.scrapers.base import BaseScraper
from app.models import Product

@pytest.mark.asyncio
async def test_fetch_page():
    scraper = BaseScraper()

    try:
        html = await scraper.fetch_page("https://www.decathlon.ua/uk/")

        assert "<html" in html.lower()
    finally:
        await scraper.close()

from unittest.mock import AsyncMock, patch

def test_scrape_decathlon(client, db_session, product_data):
    with patch(
        "app.routers.scraper.DecathlonScraper"
    ) as mock_scraper_class:

        mock_scraper = mock_scraper_class.return_value.__aenter__.return_value

        mock_scraper.fetch_and_parse_products = AsyncMock(
            return_value=[product_data]
        )

        response = client.post("/scrape/decathlon")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert data["processed"] == 1

    saved_products = db_session.query(Product).all()

    assert len(saved_products) == 1
    assert saved_products[0].name == product_data.name
