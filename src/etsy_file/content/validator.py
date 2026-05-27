import re

# Etsy API v3 content constraints
TITLE_MAX = 140
TAG_MAX_LEN = 20
TAG_MAX_COUNT = 13

_TAG_PATTERN = re.compile(r"^[A-Za-z0-9 \-]+$")


def validate_title(title: str) -> None:
    if not title.strip():
        raise ValueError("Title must not be empty")
    if len(title) > TITLE_MAX:
        raise ValueError(f"Title too long: {len(title)} chars (max {TITLE_MAX})")


def validate_tag(tag: str) -> None:
    if not tag.strip():
        raise ValueError("Tag must not be empty")
    if len(tag) > TAG_MAX_LEN:
        raise ValueError(f"Tag '{tag}' too long: {len(tag)} chars (max {TAG_MAX_LEN})")
    if not _TAG_PATTERN.match(tag):
        raise ValueError(
            f"Tag '{tag}' contains invalid characters "
            "(only letters, numbers, spaces, hyphens allowed)"
        )


def validate_tags(tags: list[str]) -> None:
    if len(tags) > TAG_MAX_COUNT:
        raise ValueError(f"Too many tags: {len(tags)} (max {TAG_MAX_COUNT})")
    for tag in tags:
        validate_tag(tag)


def validate_content(title: str, tags: list[str]) -> None:
    validate_title(title)
    validate_tags(tags)
