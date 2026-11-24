from fastapi import FastAPI
from app.routers.products import router as product_router
from app.routers.scraper import router as scraper_router
from app.database import Base, engine
from app import models

from contextlib import asynccontextmanager
from app.scheduler import start_scheduler, stop_scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)

    start_scheduler()

    yield 

    stop_scheduler()

app = FastAPI(
    title="Price tracker API",
    description="Track product prices from online stores",
    version="0.1.0",
    lifespan=lifespan
)

app.include_router(product_router)
app.include_router(scraper_router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

