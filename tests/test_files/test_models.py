from etsy_file.files.models import ListingFile


def make_file_dict(**overrides) -> dict:
    base = {
        "listing_file_id": 501,
        "listing_id": 1001,
        "filename": "daily-planner.pdf",
        "filesize": "1.2MB",
        "size_bytes": 1_258_291,
        "filetype": "application/pdf",
        "create_timestamp": 1_700_000_000,
    }
    base.update(overrides)
    return base


def test_from_api_maps_all_fields():
    f = ListingFile.from_api(make_file_dict())
    assert f.listing_file_id == 501
    assert f.listing_id == 1001
    assert f.filename == "daily-planner.pdf"
    assert f.filesize == "1.2MB"
    assert f.size_bytes == 1_258_291
    assert f.filetype == "application/pdf"
    assert f.create_timestamp == 1_700_000_000


def test_from_api_optional_fields_default():
    data = make_file_dict()
    for key in ("filesize", "size_bytes", "filetype", "create_timestamp"):
        del data[key]
    f = ListingFile.from_api(data)
    assert f.filesize == ""
    assert f.size_bytes == 0
    assert f.filetype == ""
    assert f.create_timestamp == 0
