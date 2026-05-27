from io import StringIO

import pytest
from rich.console import Console

from etsy_file.dashboard.models import ListingCounts, ShopInfo, ShopSummary
from etsy_file.dashboard.report import DashboardReport


@pytest.fixture
def summary():
    info = ShopInfo(
        shop_id=9001,
        shop_name="ThePlannersCollective",
        title="Beautiful digital planners",
        num_favorers=1234,
        review_count=567,
        review_average=4.9,
        listing_active_count=42,
        url="https://www.etsy.com/shop/ThePlannersCollective",
    )
    counts = ListingCounts(active=42, inactive=8, draft=3)
    return ShopSummary(info=info, listing_counts=counts)


@pytest.fixture
def report():
    buf = StringIO()
    console = Console(file=buf, highlight=False, markup=False)
    return DashboardReport(console=console), buf


# ------------------------------------------------------------------
# to_dict
# ------------------------------------------------------------------


def test_to_dict_contains_shop_fields(report, summary):
    r, _ = report
    data = r.to_dict(summary)
    assert data["shop_name"] == "ThePlannersCollective"
    assert data["title"] == "Beautiful digital planners"
    assert data["num_favorers"] == 1234
    assert data["review_count"] == 567
    assert data["review_average"] == 4.9


def test_to_dict_contains_listing_counts(report, summary):
    r, _ = report
    data = r.to_dict(summary)
    assert data["listings"]["active"] == 42
    assert data["listings"]["inactive"] == 8
    assert data["listings"]["draft"] == 3
    assert data["listings"]["total"] == 53


# ------------------------------------------------------------------
# print (output content)
# ------------------------------------------------------------------


def test_print_includes_shop_name(report, summary):
    r, buf = report
    r.print(summary)
    output = buf.getvalue()
    assert "ThePlannersCollective" in output


def test_print_includes_listing_counts(report, summary):
    r, buf = report
    r.print(summary)
    output = buf.getvalue()
    assert "42" in output   # active
    assert "8" in output    # inactive
    assert "3" in output    # draft
    assert "53" in output   # total


def test_print_includes_review_stats(report, summary):
    r, buf = report
    r.print(summary)
    output = buf.getvalue()
    assert "567" in output   # review count
    assert "4.9" in output   # review average


def test_print_includes_favorers(report, summary):
    r, buf = report
    r.print(summary)
    output = buf.getvalue()
    assert "1,234" in output  # formatted with comma


# ------------------------------------------------------------------
# default console
# ------------------------------------------------------------------


def test_report_uses_default_console_when_none_provided():
    r = DashboardReport()
    assert r._console is not None
