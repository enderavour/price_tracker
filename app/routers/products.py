from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.repositories.product_repository import ProductRepository
from app.schemas import ProductResponse

from app.repositories.price_repository import PriceHistoryRepository
from app.schemas import PriceHistoryResponse
from app.dependencies import get_db

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.get("/", response_model=list[ProductResponse])
def get_products(
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db)
):
    repository = ProductRepository(db)

    return repository.get_all(
        limit=limit,
        offset=offset
    )


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    repository = ProductRepository(db)

    product = repository.get_by_id(product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product


@router.get(
    "/{product_id}/history",
    response_model=list[PriceHistoryResponse]
)
def get_product_history(
    product_id: int,
    db: Session = Depends(get_db)
):
    product_repository = ProductRepository(db)
    history_repository = PriceHistoryRepository(db)

    product = product_repository.get_by_id(product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return history_repository.get_by_product_id(product_id)

