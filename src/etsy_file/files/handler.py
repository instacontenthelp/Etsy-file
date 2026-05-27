from pathlib import Path

from etsy_file.api.client import EtsyClient

from .local import validate_file
from .models import ListingFile


class FileHandler:
    def __init__(self, client: EtsyClient, shop_id: str) -> None:
        self._client = client
        self._shop_id = shop_id

    def _base(self, listing_id: int) -> str:
        return f"/application/shops/{self._shop_id}/listings/{listing_id}/files"

    def list_files(self, listing_id: int) -> list[ListingFile]:
        data = self._client.get(self._base(listing_id))
        return [ListingFile.from_api(r) for r in data.get("results", [])]

    def get_file(self, listing_id: int, file_id: int) -> ListingFile:
        data = self._client.get(f"{self._base(listing_id)}/{file_id}")
        return ListingFile.from_api(data)

    def upload_file(self, listing_id: int, file_path: Path) -> ListingFile:
        """Validate then upload *file_path* to the listing as a digital download."""
        validate_file(file_path)
        with open(file_path, "rb") as fh:
            data = self._client.post(
                self._base(listing_id),
                files={"file": (file_path.name, fh, "application/octet-stream")},
            )
        return ListingFile.from_api(data)

    def delete_file(self, listing_id: int, file_id: int) -> None:
        self._client.delete(f"{self._base(listing_id)}/{file_id}")

    def replace_file(
        self, listing_id: int, file_id: int, new_path: Path
    ) -> ListingFile:
        """Delete the existing file and upload a replacement in one step."""
        self.delete_file(listing_id, file_id)
        return self.upload_file(listing_id, new_path)
