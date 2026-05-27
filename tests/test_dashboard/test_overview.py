import pytest

from etsy_file.api.client import EtsyClient
from etsy_file.dashboard.models import ListingCounts, ShopInfo, ShopSummary
from etsy_file.dashboard.overview import ShopOverview


def make_shop_dict(**overrides) -> dict:
    base = {
        "shop_id": 9001,
        "shop_name": "ThePlannersCollective",
        "title": "Digital planners",
        "num_favorers": 500,
        "review_count": 200,
        "review_average": 4.8,
        "listing_active_count": 30,
        "url": "https://www.etsy.com/shop/ThePlannersCollective",
    }
    base.update(overrides)
    return base


@pytest.fixture
def mock_client(mocker):
    return mocker.MagicMock(spec=EtsyClient)


@pytest.fixture
def overview(mock_client):
    return ShopOverview(client=mock_client, shop_id="9001")


# ------------------------------------------------------------------
# get_shop_info
# ------------------------------------------------------------------


def test_get_shop_info_returns_shop_info(overview, mock_client):
    mock_client.get.return_value = make_shop_dict()
    info = overview.get_shop_info()
    assert isinstance(info, ShopInfo)
    assert info.shop_name == "ThePlannersCollective"
    mock_client.get.assert_called_once_with("/application/shops/9001")


# ------------------------------------------------------------------
# get_listing_counts
# ------------------------------------------------------------------


def test_get_listing_counts_fetches_all_states(overview, mock_client):
    mock_client.get.side_effect = [
        {"count": 30},   # active
        {"count": 5},    # inactive
        {"count": 2},    # draft
    ]
    counts = overview.get_listing_counts()
    assert isinstance(counts, ListingCounts)
    assert counts.active == 30
    assert counts.inactive == 5
    assert counts.draft == 2
    assert counts.total == 37
    assert mock_client.get.call_count == 3


def test_get_listing_counts_uses_limit_1(overview, mock_client):
    mock_client.get.return_value = {"count": 0}
    overview.get_listing_counts()
    for call in mock_client.get.call_args_list:
        assert call.kwargs["params"]["limit"] == 1


def test_get_listing_counts_defaults_to_zero_on_missing_count(overview, mock_client):
    mock_client.get.return_value = {}
    counts = overview.get_listing_counts()
    assert counts.active == 0
    assert counts.inactive == 0
    assert counts.draft == 0


# ------------------------------------------------------------------
# get_summary
# ------------------------------------------------------------------


def test_get_summary_returns_shop_summary(overview, mock_client):
    mock_client.get.side_effect = [
        make_shop_dict(),   # shop info
        {"count": 10},      # active
        {"count": 2},       # inactive
        {"count": 1},       # draft
    ]
    summary = overview.get_summary()
    assert isinstance(summary, ShopSummary)
    assert summary.info.shop_name == "ThePlannersCollective"
    assert summary.listing_counts.total == 13
