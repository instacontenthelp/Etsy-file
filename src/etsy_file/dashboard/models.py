from dataclasses import dataclass


@dataclass
class ShopInfo:
    shop_id: int
    shop_name: str
    title: str
    num_favorers: int
    review_count: int
    review_average: float
    listing_active_count: int
    url: str

    @classmethod
    def from_api(cls, data: dict) -> "ShopInfo":
        return cls(
            shop_id=data["shop_id"],
            shop_name=data["shop_name"],
            title=data.get("title", ""),
            num_favorers=data.get("num_favorers", 0),
            review_count=data.get("review_count", 0),
            review_average=data.get("review_average", 0.0),
            listing_active_count=data.get("listing_active_count", 0),
            url=data.get("url", ""),
        )


@dataclass
class ListingCounts:
    active: int
    inactive: int
    draft: int

    @property
    def total(self) -> int:
        return self.active + self.inactive + self.draft


@dataclass
class ShopSummary:
    info: ShopInfo
    listing_counts: ListingCounts
