import pytest

from etsy_file.listings.models import Listing, ListingPrice


def make_listing_dict(**overrides) -> dict:
    base = {
        "listing_id": 1001,
        "shop_id": 9001,
        "title": "Daily Planner PDF",
        "description": "A beautiful daily planner.",
        "state": "active",
        "quantity": 999,
        "tags": ["planner", "digital", "printable"],
        "price": {"amount": 499, "divisor": 100, "currency_code": "USD"},
        "url": "https://www.etsy.com/listing/1001",
        "taxonomy_id": 2078,
    }
    base.update(overrides)
    return base


# ------------------------------------------------------------------
# ListingPrice
# ------------------------------------------------------------------


def test_price_value():
    price = ListingPrice(amount=499, divisor=100, currency_code="USD")
    assert price.value == pytest.approx(4.99)


def test_price_from_api():
    price = ListingPrice.from_api({"amount": 1000, "divisor": 100, "currency_code": "GBP"})
    assert price.value == pytest.approx(10.0)
    assert price.currency_code == "GBP"


def test_price_from_api_empty_dict_uses_defaults():
    price = ListingPrice.from_api({})
    assert price.amount == 0
    assert price.divisor == 100
    assert price.currency_code == "USD"


# ------------------------------------------------------------------
# Listing
# ------------------------------------------------------------------


def test_listing_from_api():
    listing = Listing.from_api(make_listing_dict())
    assert listing.listing_id == 1001
    assert listing.shop_id == 9001
    assert listing.title == "Daily Planner PDF"
    assert listing.state == "active"
    assert listing.quantity == 999
    assert listing.tags == ["planner", "digital", "printable"]
    assert listing.price.value == pytest.approx(4.99)
    assert listing.url == "https://www.etsy.com/listing/1001"
    assert listing.taxonomy_id == 2078


def test_listing_from_api_optional_fields_default():
    data = make_listing_dict()
    del data["tags"]
    del data["url"]
    del data["taxonomy_id"]
    listing = Listing.from_api(data)
    assert listing.tags == []
    assert listing.url == ""
    assert listing.taxonomy_id is None
