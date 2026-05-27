import pytest
from pathlib import Path

from etsy_file.files.local import (
    ALLOWED_EXTENSIONS,
    MAX_FILES_PER_LISTING,
    rename_file,
    scan_directory,
    validate_file,
)


# ------------------------------------------------------------------
# scan_directory
# ------------------------------------------------------------------


def test_scan_directory_returns_allowed_files(tmp_path):
    (tmp_path / "planner.pdf").write_bytes(b"pdf")
    (tmp_path / "cover.png").write_bytes(b"png")
    (tmp_path / "notes.txt").write_bytes(b"txt")  # not allowed

    files = scan_directory(tmp_path)

    names = {f.name for f in files}
    assert "planner.pdf" in names
    assert "cover.png" in names
    assert "notes.txt" not in names


def test_scan_directory_custom_extension_filter(tmp_path):
    (tmp_path / "file.pdf").write_bytes(b"pdf")
    (tmp_path / "file.zip").write_bytes(b"zip")

    files = scan_directory(tmp_path, extensions={".zip"})

    assert len(files) == 1
    assert files[0].name == "file.zip"


def test_scan_directory_returns_sorted_results(tmp_path):
    for name in ("c.pdf", "a.pdf", "b.pdf"):
        (tmp_path / name).write_bytes(b"x")

    files = scan_directory(tmp_path)
    assert [f.name for f in files] == ["a.pdf", "b.pdf", "c.pdf"]


def test_scan_directory_empty(tmp_path):
    assert scan_directory(tmp_path) == []


# ------------------------------------------------------------------
# validate_file
# ------------------------------------------------------------------


def test_validate_file_accepts_pdf(tmp_path):
    f = tmp_path / "planner.pdf"
    f.write_bytes(b"content")
    validate_file(f)  # should not raise


def test_validate_file_rejects_missing_file(tmp_path):
    with pytest.raises(ValueError, match="not found"):
        validate_file(tmp_path / "ghost.pdf")


def test_validate_file_rejects_unsupported_extension(tmp_path):
    f = tmp_path / "notes.txt"
    f.write_bytes(b"hello")
    with pytest.raises(ValueError, match="Unsupported file type"):
        validate_file(f)


def test_validate_file_rejects_oversized_file(tmp_path, monkeypatch):
    f = tmp_path / "big.pdf"
    f.write_bytes(b"x")

    monkeypatch.setattr(
        "etsy_file.files.local._MAX_FILE_BYTES", 5
    )
    f.write_bytes(b"x" * 10)

    with pytest.raises(ValueError, match="too large"):
        validate_file(f)


def test_validate_file_rejects_directory(tmp_path):
    d = tmp_path / "subdir"
    d.mkdir()
    # directories have no extension — hits the extension check first
    with pytest.raises(ValueError):
        validate_file(d)


# ------------------------------------------------------------------
# rename_file
# ------------------------------------------------------------------


def test_rename_file_keeps_extension(tmp_path):
    original = tmp_path / "old-name.pdf"
    original.write_bytes(b"pdf")

    new_path = rename_file(original, "new-name")

    assert new_path.name == "new-name.pdf"
    assert new_path.exists()
    assert not original.exists()


def test_rename_file_returns_new_path(tmp_path):
    f = tmp_path / "before.zip"
    f.write_bytes(b"zip")
    result = rename_file(f, "after")
    assert result == tmp_path / "after.zip"


# ------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------


def test_max_files_per_listing():
    assert MAX_FILES_PER_LISTING == 5


def test_pdf_in_allowed_extensions():
    assert ".pdf" in ALLOWED_EXTENSIONS
