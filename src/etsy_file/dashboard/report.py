from io import StringIO

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .models import ShopSummary


class DashboardReport:
    def __init__(self, console: Console | None = None) -> None:
        self._console = console or Console()

    def print(self, summary: ShopSummary) -> None:
        self._console.print(self._shop_panel(summary))
        self._console.print(self._listings_table(summary))

    def to_dict(self, summary: ShopSummary) -> dict:
        return {
            "shop_name": summary.info.shop_name,
            "title": summary.info.title,
            "num_favorers": summary.info.num_favorers,
            "review_count": summary.info.review_count,
            "review_average": summary.info.review_average,
            "listings": {
                "active": summary.listing_counts.active,
                "inactive": summary.listing_counts.inactive,
                "draft": summary.listing_counts.draft,
                "total": summary.listing_counts.total,
            },
        }

    def _shop_panel(self, summary: ShopSummary) -> Panel:
        info = summary.info
        lines = [
            f"[bold]{info.shop_name}[/bold]",
            info.title,
            "",
            f"Favorers: [cyan]{info.num_favorers:,}[/cyan]  |  "
            f"Reviews: [cyan]{info.review_count:,}[/cyan] "
            f"([yellow]{info.review_average:.1f}★[/yellow])",
        ]
        return Panel("\n".join(lines), title="Shop Overview", expand=False)

    def _listings_table(self, summary: ShopSummary) -> Table:
        counts = summary.listing_counts
        table = Table(title="Listings", box=box.SIMPLE, show_footer=False)
        table.add_column("State", style="cyan", no_wrap=True)
        table.add_column("Count", justify="right")
        table.add_row("Active", str(counts.active))
        table.add_row("Inactive", str(counts.inactive))
        table.add_row("Draft", str(counts.draft))
        table.add_row("[bold]Total[/bold]", f"[bold]{counts.total}[/bold]")
        return table
