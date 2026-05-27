import pytest
from pathlib import Path

from etsy_file.api.client import EtsyClient
from etsy_file.files.handler import FileHandler
from etsy_file.files.models import ListingFile


def make_file_dict(file_id: int = 501, **overrides) -> dict:
    base = {
        "listing_file_id": file_id,
        "listing_id": 1001,
        "filename": "planner.pdf",
        "filesize": "512KB",
        "size_bytes": 524_288,
        "filetype": "application/pdf",
        "create_timestamp": 1_700_000_000,
    }
    base.update(overrides)
    return base


@pytest.fixture
def mock_client(mocker):
    return mocker.MagicMock(spec=EtsyClient)


@pytest.fixture
def handler(mock_client):
    return FileHandler(client=mock_client, shop_id="9001")


@pytest.fixture
def pdf_file(tmp_path) -> Path:
    f = tmp_path / "planner.pdf"
    f.write_bytes(b"%PDF content")
    return f


# ------------------------------------------------------------------
# list_files
# ------------------------------------------------------------------


def test_list_files_returns_listing_files(handler, mock_client):
    mock_client.get.return_value = {
        "results": [make_file_dict(501), make_file_dict(502)]
    }
    files = handler.list_files(1001)
    assert len(files) == 2
    assert all(isinstance(f, ListingFile) for f in files)
    mock_client.get.assert_called_once_with(
        "/application/shops/9001/listings/1001/files"
    )


def test_list_files_empty(handler, mock_client):
    mock_client.get.return_value = {"results": []}
    assert handler.list_files(1001) == []


# ------------------------------------------------------------------
# get_file
# ------------------------------------------------------------------


def test_get_file_returns_single_file(handler, mock_client):
    mock_client.get.return_value = make_file_dict(501)
    f = handler.get_file(1001, 501)
    assert isinstance(f, ListingFile)
    assert f.listing_file_id == 501
    mock_client.get.assert_called_once_with(
        "/application/shops/9001/listings/1001/files/501"
    )


# ------------------------------------------------------------------
# upload_file
# ------------------------------------------------------------------


def test_upload_file_validates_then_posts(handler, mock_client, pdf_file):
    mock_client.post.return_value = make_file_dict(601, filename=pdf_file.name)

    result = handler.upload_file(1001, pdf_file)

    assert isinstance(result, ListingFile)
    assert result.listing_file_id == 601
    mock_client.post.assert_called_once()
    call_kwargs = mock_client.post.call_args
    assert call_kwargs.args[0] == "/application/shops/9001/listings/1001/files"
    assert "files" in call_kwargs.kwargs
    assert "file" in call_kwargs.kwargs["files"]


def test_upload_file_rejects_invalid_extension(handler, tmp_path):
    bad_file = tmp_path / "notes.txt"
    bad_file.write_bytes(b"hello")
    with pytest.raises(ValueError, match="Unsupported file type"):
        handler.upload_file(1001, bad_file)


def test_upload_file_rejects_missing_file(handler, tmp_path):
    with pytest.raises(ValueError, match="not found"):
        handler.upload_file(1001, tmp_path / "ghost.pdf")


# ------------------------------------------------------------------
# delete_file
# ------------------------------------------------------------------


def test_delete_file_calls_delete_endpoint(handler, mock_client):
    handler.delete_file(1001, 501)
    mock_client.delete.assert_called_once_with(
        "/application/shops/9001/listings/1001/files/501"
    )


# ------------------------------------------------------------------
# replace_file
# ------------------------------------------------------------------


def test_replace_file_deletes_old_then_uploads_new(handler, mock_client, pdf_file):
    mock_client.post.return_value = make_file_dict(602, filename=pdf_file.name)

    result = handler.replace_file(1001, 501, pdf_file)

    mock_client.delete.assert_called_once_with(
        "/application/shops/9001/listings/1001/files/501"
    )
    mock_client.post.assert_called_once()
    assert result.listing_file_id == 602
