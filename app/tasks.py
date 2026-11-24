import logging

from app.database import SessionLocal
from app.scrapers.decathlon import DecathlonScraper
from app.services.product_service import ProductService
from app.uow import ProductPriceUOW

logger = logging.getLogger(__name__)


async def run_price_update():
    logger.info("Starting scheduled price update")

    try:
        async with DecathlonScraper() as scraper:
            products = await scraper.fetch_and_parse_products(27418)

        if not products:
            logger.warning("No products found during scheduled update")
            return

        db = SessionLocal()

        with ProductPriceUOW(db) as uow:
            service = ProductService(uow)
            service.process_products(products)

        logger.info(
            "Scheduled price update completed. Processed: %s",
            len(products)
        )

    except Exception:
        logger.exception("Scheduled price update failed")