
import logging

import httpx

logger = logging.getLogger(__name__)


class BaseScraper:
    def __init__(self):
        self.client = httpx.AsyncClient(
            timeout=15.0,
            follow_redirects=True,
            headers={
                "User-Agent": "PriceTracker/1.0"
            }
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.close()

    async def fetch_page(self, url: str) -> str:
        response = await self.client.get(url)
        response.raise_for_status()
        return response.text

    async def fetch_json(
        self,
        url: str,
        payload: dict,
        headers: dict[str, str]
    ) -> dict:
        try:
            response = await self.client.post(
                url,
                json=payload,
                headers=headers
            )

            response.raise_for_status()

            return response.json()

        except httpx.TimeoutException:
            logger.exception("Request to external API timed out")
            raise

        except httpx.HTTPStatusError as exc:
            logger.error(
                "External API returned HTTP %s: %s",
                exc.response.status_code,
                exc.response.text
            )
            raise

        except httpx.RequestError:
            logger.exception("Network error while connecting to external API")
            raise

        except ValueError:
            logger.exception("External API returned invalid JSON")
            raise

    async def close(self):
        await self.client.aclose()
