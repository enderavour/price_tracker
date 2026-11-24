from .base import BaseScraper
from app.schemas import ProductData
from app.config import settings
from urllib.parse import quote
from decimal import Decimal

class DecathlonScraper(BaseScraper):
    def __init__(self):
        super().__init__()

    async def fetch_and_parse_products(
        self, 
        category_id: int,
        hits_per_page: int = 20
    ) -> list[ProductData]:
        headers = {
            "x-algolia-application-id": settings.algolia_app_id,
            "x-algolia-api-key": settings.algolia_api_key,
            "Content-Type": "application/json",
        }

        products = []
        
        payload = self.build_payload(category_id=category_id, page_num=0, hits_per_page=hits_per_page)

        result = await self.fetch_json(settings.algolia_app_url, payload, headers)

        search_result = self.extract_search_result(result)

        hits = search_result["hits"]

        products.extend(self.serialize_hit(hit) for hit in hits)

        num_pages = int(search_result["nbPages"])

        for page_num in range(1, num_pages):
            payload = self.build_payload(category_id=category_id, page_num=page_num, hits_per_page=hits_per_page)

            result = await self.fetch_json(settings.algolia_app_url, payload, headers)

            search_result = self.extract_search_result(result)

            hits = search_result["hits"]

            products.extend(self.serialize_hit(hit) for hit in hits)

        return products

    def build_payload(self, category_id: int, page_num: int, hits_per_page: int) -> dict:
        rule_contexts = quote(f'["category_{category_id}"]')
        filters = quote(f"category = {category_id}")

        payload = {
            "requests": [
                {
                    "indexName": "prod_oneshop",
                    "params": (
                        f"ruleContexts={rule_contexts}"
                        "&clickAnalytics=true"
                        "&distinct=true"
                        f"&filters={filters}"
                        f"&page={page_num}"
                        f"&hitsPerPage={hits_per_page}"
                    ),
                }
            ]
        }

        return payload

    def extract_search_result(self, result: dict) -> dict:
        try:
            search_result = result["results"][0]
            hits = search_result["hits"]
            pages = search_result["nbPages"]

            if not isinstance(hits, list):
                raise ValueError("Algolia hits must be a list")

            if not isinstance(pages, int):
                raise ValueError("nbPages must be an integer")

            return search_result

        except (KeyError, IndexError, TypeError) as e:
            raise ValueError("Invalid Algolia response structure") from e


    def serialize_hit(self, hit: dict) -> ProductData:
        return ProductData(
            source_id=hit["id_code_article"],
            source="decathlon",
            name=hit["product_name"]["uk"],
            brand=hit.get("brand"),
            price=Decimal(hit["prix"]),
            regular_price=hit.get("regular"),
            currency=hit["currency"],
            category=hit["nature"]["uk"],
            url=f"https://www.decathlon.ua{hit['url']['uk']}",
            image_url=hit.get("image_url"),
            available=hit.get("available", 0) == 1
        )


