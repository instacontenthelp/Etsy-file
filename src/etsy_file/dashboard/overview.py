from etsy_file.api.client import EtsyClient

from .models import ListingCounts, ShopInfo, ShopSummary


class ShopOverview:
    def __init__(self, client: EtsyClient, shop_id: str) -> None:
        self._client = client
        self._shop_id = shop_id

    def get_shop_info(self) -> ShopInfo:
        data = self._client.get(f"/application/shops/{self._shop_id}")
        return ShopInfo.from_api(data)

    def get_listing_counts(self) -> ListingCounts:
        def _count(state: str) -> int:
            data = self._client.get(
                f"/application/shops/{self._shop_id}/listings",
                params={"state": state, "limit": 1},
            )
            return data.get("count", 0)

        return ListingCounts(
            active=_count("active"),
            inactive=_count("inactive"),
            draft=_count("draft"),
        )

    def get_summary(self) -> ShopSummary:
        return ShopSummary(
            info=self.get_shop_info(),
            listing_counts=self.get_listing_counts(),
        )
