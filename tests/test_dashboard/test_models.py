from etsy_file.dashboard.models import ListingCounts, ShopInfo, ShopSummary


def make_shop_dict(**overrides) -> dict:
    base = {
        "shop_id": 9001,
        "shop_name": "ThePlannersCollective",
        "title": "Beautiful digital planners for every day",
        "num_favorers": 1234,
        "review_count": 567,
        "review_average": 4.9,
        "listing_active_count": 42,
        "url": "https://www.etsy.com/shop/ThePlannersCollective",
    }
    base.update(overrides)
    return base


# ------------------------------------------------------------------
# ShopInfo
# ------------------------------------------------------------------


def test_shop_info_from_api_maps_all_fields():
    info = ShopInfo.from_api(make_shop_dict())
    assert info.shop_id == 9001
    assert info.shop_name == "ThePlannersCollective"
    assert info.title == "Beautiful digital planners for every day"
    assert info.num_favorers == 1234
    assert info.review_count == 567
    assert info.review_average == 4.9
    assert info.listing_active_count == 42
    assert "etsy.com" in info.url


def test_shop_info_from_api_optional_fields_default():
    data = {"shop_id": 1, "shop_name": "MyShop"}
    info = ShopInfo.from_api(data)
    assert info.title == ""
    assert info.num_favorers == 0
    assert info.review_count == 0
    assert info.review_average == 0.0
    assert info.listing_active_count == 0
    assert info.url == ""


# ------------------------------------------------------------------
# ListingCounts
# ------------------------------------------------------------------


def test_listing_counts_total():
    counts = ListingCounts(active=10, inactive=3, draft=2)
    assert counts.total == 15


def test_listing_counts_total_all_zero():
    assert ListingCounts(active=0, inactive=0, draft=0).total == 0


# ------------------------------------------------------------------
# ShopSummary
# ------------------------------------------------------------------


def test_shop_summary_holds_info_and_counts():
    info = ShopInfo.from_api(make_shop_dict())
    counts = ListingCounts(active=10, inactive=2, draft=1)
    summary = ShopSummary(info=info, listing_counts=counts)
    assert summary.info.shop_name == "ThePlannersCollective"
    assert summary.listing_counts.total == 13
