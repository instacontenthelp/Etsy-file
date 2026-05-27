from collections.abc import Iterator

from etsy_file.api.client import EtsyClient

from .models import Listing

_PAGE_SIZE = 100


class ListingManager:
    def __init__(self, client: EtsyClient, shop_id: str) -> None:
        self._client = client
        self._shop_id = shop_id

    def get(self, listing_id: int) -> Listing:
        data = self._client.get(f"/application/listings/{listing_id}")
        return Listing.from_api(data)

    def list_active(
        self, limit: int = 25, offset: int = 0
    ) -> tuple[list[Listing], int]:
        """Return (page_of_listings, total_count) for the shop's active listings."""
        data = self._client.get(
            f"/application/shops/{self._shop_id}/listings/active",
            params={"limit": limit, "offset": offset},
        )
        listings = [Listing.from_api(r) for r in data.get("results", [])]
        return listings, data.get("count", 0)

    def list_all(self) -> Iterator[Listing]:
        """Yield every active listing, fetching pages automatically."""
        offset = 0
        while True:
            listings, total = self.list_active(limit=_PAGE_SIZE, offset=offset)
            yield from listings
            offset += _PAGE_SIZE
            if offset >= total:
                break

    def create(self, payload: dict) -> Listing:
        data = self._client.post(
            f"/application/shops/{self._shop_id}/listings",
            json=payload,
        )
        return Listing.from_api(data)

    def update(self, listing_id: int, payload: dict) -> Listing:
        data = self._client.patch(
            f"/application/listings/{listing_id}",
            json=payload,
        )
        return Listing.from_api(data)

    def delete(self, listing_id: int) -> None:
        self._client.delete(f"/application/listings/{listing_id}")

    def bulk_update(self, updates: list[tuple[int, dict]]) -> list[Listing]:
        """Update multiple listings in order. Returns results matching the input order."""
        return [self.update(lid, payload) for lid, payload in updates]
