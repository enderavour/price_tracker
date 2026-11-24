from app.database import SessionLocal
from app.scrapers.decathlon import DecathlonScraper
from app.services.product_service import ProductService
from app.uow import ProductPriceUOW
import asyncio

async def run_decathlon_scraper():
    async with DecathlonScraper() as scraper:
        products = await scraper.fetch_and_parse_products(27418)

        if not products:
            print("No products found.")
            return

        db = SessionLocal()

        with ProductPriceUOW(db) as uow:
            service = ProductService(uow)
            service.process_products(products)


if __name__ == "__main__":
    asyncio.run(run_decathlon_scraper())