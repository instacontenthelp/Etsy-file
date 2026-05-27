import pytest

from etsy_file.content.validator import (
    TITLE_MAX,
    TAG_MAX_COUNT,
    TAG_MAX_LEN,
    validate_content,
    validate_tag,
    validate_tags,
    validate_title,
)


# ------------------------------------------------------------------
# validate_title
# ------------------------------------------------------------------


def test_validate_title_accepts_normal_title():
    validate_title("Daily Planner 2025 | Printable PDF")  # no raise


def test_validate_title_rejects_empty():
    with pytest.raises(ValueError, match="empty"):
        validate_title("")


def test_validate_title_rejects_whitespace_only():
    with pytest.raises(ValueError, match="empty"):
        validate_title("   ")


def test_validate_title_rejects_over_limit():
    with pytest.raises(ValueError, match="too long"):
        validate_title("A" * (TITLE_MAX + 1))


def test_validate_title_accepts_exactly_at_limit():
    validate_title("A" * TITLE_MAX)  # no raise


# ------------------------------------------------------------------
# validate_tag
# ------------------------------------------------------------------


def test_validate_tag_accepts_simple_tag():
    validate_tag("planner")  # no raise


def test_validate_tag_accepts_tag_with_space():
    validate_tag("daily planner")  # no raise


def test_validate_tag_accepts_tag_with_hyphen():
    validate_tag("to-do list")  # no raise


def test_validate_tag_rejects_empty():
    with pytest.raises(ValueError, match="empty"):
        validate_tag("")


def test_validate_tag_rejects_over_20_chars():
    with pytest.raises(ValueError, match="too long"):
        validate_tag("A" * (TAG_MAX_LEN + 1))


def test_validate_tag_accepts_exactly_20_chars():
    validate_tag("A" * TAG_MAX_LEN)  # no raise


def test_validate_tag_rejects_special_characters():
    with pytest.raises(ValueError, match="invalid characters"):
        validate_tag("planner@2025")


def test_validate_tag_rejects_comma():
    with pytest.raises(ValueError, match="invalid characters"):
        validate_tag("planner, pdf")


# ------------------------------------------------------------------
# validate_tags
# ------------------------------------------------------------------


def test_validate_tags_accepts_valid_list():
    validate_tags(["planner", "digital", "printable"])  # no raise


def test_validate_tags_accepts_empty_list():
    validate_tags([])  # no raise


def test_validate_tags_rejects_too_many():
    with pytest.raises(ValueError, match="Too many tags"):
        validate_tags(["tag"] * (TAG_MAX_COUNT + 1))


def test_validate_tags_accepts_exactly_max():
    validate_tags([f"tag{i}" for i in range(TAG_MAX_COUNT)])  # no raise


def test_validate_tags_propagates_single_tag_error():
    with pytest.raises(ValueError, match="invalid characters"):
        validate_tags(["good-tag", "bad@tag"])


# ------------------------------------------------------------------
# validate_content
# ------------------------------------------------------------------


def test_validate_content_valid():
    validate_content("My Planner", ["planner", "digital"])  # no raise


def test_validate_content_fails_on_bad_title():
    with pytest.raises(ValueError):
        validate_content("", ["planner"])


def test_validate_content_fails_on_bad_tags():
    with pytest.raises(ValueError):
        validate_content("Fine Title", ["bad@tag"])
