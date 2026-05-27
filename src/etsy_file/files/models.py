from dataclasses import dataclass


@dataclass
class ListingFile:
    listing_file_id: int
    listing_id: int
    filename: str
    filesize: str       # human-readable, e.g. "1.2MB"
    size_bytes: int
    filetype: str       # MIME type, e.g. "application/pdf"
    create_timestamp: int

    @classmethod
    def from_api(cls, data: dict) -> "ListingFile":
        return cls(
            listing_file_id=data["listing_file_id"],
            listing_id=data["listing_id"],
            filename=data["filename"],
            filesize=data.get("filesize", ""),
            size_bytes=data.get("size_bytes", 0),
            filetype=data.get("filetype", ""),
            create_timestamp=data.get("create_timestamp", 0),
        )
