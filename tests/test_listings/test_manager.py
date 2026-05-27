import pytest

from etsy_file.api.client import EtsyClient
from etsy_file.listings.manager import ListingManager
from etsy_file.listings.models import Listing


def make_listing_dict(listing_id: int = 1001, **overrides) -> dict:
    base = {
        "listing_id": listing_id,
        "shop_id": 9001,
        "title": "Daily Planner PDF",
        "description": "A beautiful daily planner.",
        "state": "active",
        "quantity": 999,
        "tags": ["planner", "digital"],
        "price": {"amount": 499, "divisor": 100, "currency_code": "USD"},
        "url": f"https://www.etsy.com/listing/{listing_id}",
        "taxonomy_id": 2078,
    }
    base.update(overrides)
    return base


@pytest.fixture
def mock_client(mocker):
    client = mocker.MagicMock(spec=EtsyClient)
    return client


@pytest.fixture
def manager(mock_client):
    return ListingManager(client=mock_client, shop_id="9001")


# ------------------------------------------------------------------
# get
# ------------------------------------------------------------------


def test_get_returns_listing(manager, mock_client):
    mock_client.get.return_value = make_listing_dict(1001)
    listing = manager.get(1001)
    assert isinstance(listing, Listing)
    assert listing.listing_id == 1001
    mock_client.get.assert_called_once_with("/application/listings/1001")


# ------------------------------------------------------------------
# list_active
# ------------------------------------------------------------------


def test_list_active_returns_listings_and_count(manager, mock_client):
    mock_client.get.return_value = {
        "count": 2,
        "results": [make_listing_dict(1), make_listing_dict(2)],
    }
    listings, total = manager.list_active(limit=25, offset=0)
    assert len(listings) == 2
    assert total == 2
    assert all(isinstance(l, Listing) for l in listings)


def test_list_active_passes_pagination_params(manager, mock_client):
    mock_client.get.return_value = {"count": 0, "results": []}
    manager.list_active(limit=10, offset=50)
    mock_client.get.assert_called_once_with(
        "/application/shops/9001/listings/active",
        params={"limit": 10, "offset": 50},
    )


def test_list_active_empty_shop(manager, mock_client):
    mock_client.get.return_value = {"count": 0, "results": []}
    listings, total = manager.list_active()
    assert listings == []
    assert total == 0


# ------------------------------------------------------------------
# list_all (pagination)
# ------------------------------------------------------------------


def test_list_all_yields_all_pages(manager, mock_client):
    page1 = {
        "count": 150,
        "results": [make_listing_dict(i) for i in range(100)],
    }
    page2 = {
        "count": 150,
        "results": [make_listing_dict(i) for i in range(100, 150)],
    }
    mock_client.get.side_effect = [page1, page2]

    all_listings = list(manager.list_all())

    assert len(all_listings) == 150
    assert mock_client.get.call_count == 2


def test_list_all_single_page(manager, mock_client):
    mock_client.get.return_value = {
        "count": 3,
        "results": [make_listing_dict(i) for i in range(3)],
    }
    all_listings = list(manager.list_all())
    assert len(all_listings) == 3
    assert mock_client.get.call_count == 1


def test_list_all_empty(manager, mock_client):
    mock_client.get.return_value = {"count": 0, "results": []}
    assert list(manager.list_all()) == []


# ------------------------------------------------------------------
# create
# ------------------------------------------------------------------


def test_create_posts_payload_and_returns_listing(manager, mock_client):
    mock_client.post.return_value = make_listing_dict(2000)
    payload = {
        "title": "New Planner",
        "description": "Desc",
        "price": 4.99,
        "who_made": "i_did",
        "when_made": "made_to_order",
        "taxonomy_id": 2078,
        "quantity": 999,
    }
    listing = manager.create(payload)
    assert listing.listing_id == 2000
    mock_client.post.assert_called_once_with(
        "/application/shops/9001/listings", json=payload
    )


# ------------------------------------------------------------------
# update
# ------------------------------------------------------------------


def test_update_patches_listing_and_returns_updated(manager, mock_client):
    mock_client.patch.return_value = make_listing_dict(1001, title="Updated Title")
    listing = manager.update(1001, {"title": "Updated Title"})
    assert listing.title == "Updated Title"
    mock_client.patch.assert_called_once_with(
        "/application/listings/1001", json={"title": "Updated Title"}
    )


# ------------------------------------------------------------------
# delete
# ------------------------------------------------------------------


def test_delete_calls_delete_endpoint(manager, mock_client):
    manager.delete(1001)
    mock_client.delete.assert_called_once_with("/application/listings/1001")


# ------------------------------------------------------------------
# bulk_update
# ------------------------------------------------------------------


def test_bulk_update_returns_results_in_order(manager, mock_client):
    mock_client.patch.side_effect = [
        make_listing_dict(1, title="A"),
        make_listing_dict(2, title="B"),
    ]
    results = manager.bulk_update(
        [(1, {"title": "A"}), (2, {"title": "B"})]
    )
    assert len(results) == 2
    assert results[0].title == "A"
    assert results[1].title == "B"
    assert mock_client.patch.call_count == 2


def test_bulk_update_empty_list(manager, mock_client):
    results = manager.bulk_update([])
    assert results == []
    mock_client.patch.assert_not_called()
