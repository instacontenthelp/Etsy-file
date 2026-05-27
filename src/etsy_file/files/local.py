from pathlib import Path

_MAX_FILE_BYTES = 20 * 1024 * 1024   # 20 MB — Etsy hard limit
MAX_FILES_PER_LISTING = 5

ALLOWED_EXTENSIONS = {
    ".pdf", ".png", ".jpg", ".jpeg", ".gif", ".svg",
    ".zip", ".mobi", ".epub",
    ".avi", ".flv", ".mov", ".mp4", ".mpeg", ".ogg", ".webm",
}


def scan_directory(
    path: Path, extensions: set[str] | None = None
) -> list[Path]:
    """Return files in *path*, optionally filtered to the given extensions."""
    exts = extensions or ALLOWED_EXTENSIONS
    return sorted(
        f for f in path.iterdir() if f.is_file() and f.suffix.lower() in exts
    )


def validate_file(path: Path) -> None:
    """Raise ValueError if the file cannot be uploaded to Etsy."""
    if not path.exists():
        raise ValueError(f"File not found: {path}")
    if not path.is_file():
        raise ValueError(f"Not a file: {path}")
    if path.suffix.lower() not in ALLOWED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type '{path.suffix}'. "
            f"Allowed: {', '.join(sorted(ALLOWED_EXTENSIONS))}"
        )
    size = path.stat().st_size
    if size > _MAX_FILE_BYTES:
        raise ValueError(f"File too large: {size / 1_048_576:.1f} MB (max 20 MB)")


def rename_file(path: Path, new_stem: str) -> Path:
    """Rename *path* to *new_stem* + original extension, in place."""
    new_path = path.with_name(new_stem + path.suffix)
    path.rename(new_path)
    return new_path
