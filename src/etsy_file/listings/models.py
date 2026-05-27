from dataclasses import dataclass


@dataclass
class ListingPrice:
    amount: int        # minor units (e.g. 999 = $9.99)
    divisor: int       # usually 100
    currency_code: str

    @property
    def value(self) -> float:
        return self.amount / self.divisor

    @classmethod
    def from_api(cls, data: dict) -> "ListingPrice":
        return cls(
            amount=data.get("amount", 0),
            divisor=data.get("divisor", 100),
            currency_code=data.get("currency_code", "USD"),
        )


@dataclass
class Listing:
    listing_id: int
    shop_id: int
    title: str
    description: str
    state: str
    quantity: int
    tags: list[str]
    price: ListingPrice
    url: str
    taxonomy_id: int | None = None

    @classmethod
    def from_api(cls, data: dict) -> "Listing":
        return cls(
            listing_id=data["listing_id"],
            shop_id=data["shop_id"],
            title=data["title"],
            description=data["description"],
            state=data["state"],
            quantity=data["quantity"],
            tags=data.get("tags", []),
            price=ListingPrice.from_api(data.get("price", {})),
            url=data.get("url", ""),
            taxonomy_id=data.get("taxonomy_id"),
        )
