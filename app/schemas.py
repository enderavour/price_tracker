from pydantic import BaseModel, HttpUrl, Field, ConfigDict
from decimal import Decimal
from datetime import datetime

class ProductData(BaseModel):
    source_id: str
    source: str
    name: str 
    brand: str | None = None 
    available: bool

    price: Decimal = Field(gt=0)
    regular_price: Decimal | None = None 
    currency: str = Field(min_length=3, max_length=3)

    category: str 
    url: HttpUrl
    image_url: HttpUrl | None = None 


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    source_id: str
    source: str
    name: str
    brand: str | None
    price: Decimal
    regular_price: Decimal | None 
    currency: str
    category: str
    url: str
    image_url: str | None 
    available: bool


class PriceHistoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    price: Decimal
    recorded_at: datetime


class ScrapeResponse(BaseModel):
    status: str
    message: str
    processed: int