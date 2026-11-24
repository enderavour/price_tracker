from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import SQLAlchemyError

from app.database import SessionLocal
from app.scrapers.decathlon import DecathlonScraper
from app.services.product_service import ProductService
from app.uow import ProductPriceUOW
from app.schemas import ScrapeResponse
from app.dependencies import get_db

router = APIRouter(
    prefix="/scrape",
    tags=["Scraping"]
)

@router.post("/decathlon", response_model=ScrapeResponse)
async def scrape_decathlon(
    category_id: int = 27418,
    db = Depends(get_db)
):
    async with DecathlonScraper() as scraper:
        try:
            products = await scraper.fetch_and_parse_products(category_id)
        except Exception as exc:
            raise HTTPException(
                status_code=502,
                detail="Failed to fetch products from Decathlon"
            ) from exc

        if not products:
            return {
                "status": "success",
                "message": "No products found",
                "processed": 0
            }


        try:
            with ProductPriceUOW(db) as uow:
                service = ProductService(uow)
                service.process_products(products)
        except SQLAlchemyError as exc:
            raise HTTPException(
                status_code=500,
                detail="Failed to save products to database"
            ) from exc

        return {
            "status": "success",
            "message": "Scraping completed",
            "processed": len(products)
        }
