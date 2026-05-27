import pytest

from etsy_file.content.generator import ContentGenerator
from etsy_file.content.templates import ListingTemplate
from etsy_file.content.validator import TAG_MAX_COUNT, TAG_MAX_LEN


@pytest.fixture
def template():
    return ListingTemplate(
        name="planner",
        title_template="{name} | Digital Planner PDF",
        description_template="Beautiful {name} for {year}.",
        base_tags=["planner", "printable"],
    )


@pytest.fixture
def generator(template):
    return ContentGenerator(template)


# ------------------------------------------------------------------
# render
# ------------------------------------------------------------------


def test_render_returns_valid_content(generator):
    content = generator.render({"name": "Daily Planner", "year": "2025"})
    assert content.title == "Daily Planner | Digital Planner PDF"
    assert "Daily Planner" in content.description
    assert "planner" in content.tags


def test_render_raises_on_title_too_long():
    tmpl = ListingTemplate(
        name="long",
        title_template="{padding} planner",
        description_template="desc",
        base_tags=[],
    )
    gen = ContentGenerator(tmpl)
    with pytest.raises(ValueError, match="too long"):
        gen.render({"padding": "A" * 140})


def test_render_raises_on_too_many_tags():
    tmpl = ListingTemplate(
        name="taggy",
        title_template="Planner",
        description_template="desc",
        base_tags=[f"tag{i}" for i in range(TAG_MAX_COUNT + 1)],
    )
    gen = ContentGenerator(tmpl)
    with pytest.raises(ValueError, match="Too many tags"):
        gen.render({})


# ------------------------------------------------------------------
# merge_tags
# ------------------------------------------------------------------


def test_merge_tags_combines_lists():
    result = ContentGenerator.merge_tags(["planner", "digital"], ["printable", "pdf"])
    assert result == ["planner", "digital", "printable", "pdf"]


def test_merge_tags_deduplicates_case_insensitively():
    result = ContentGenerator.merge_tags(["Planner", "digital"], ["planner", "PDF"])
    assert result.count("planner") + result.count("Planner") == 1
    assert len(result) == 3


def test_merge_tags_caps_at_13():
    big_list = [f"tag{i}" for i in range(20)]
    result = ContentGenerator.merge_tags(big_list)
    assert len(result) == TAG_MAX_COUNT


def test_merge_tags_truncates_long_tags():
    long_tag = "A" * 30
    result = ContentGenerator.merge_tags([long_tag])
    assert len(result[0]) == TAG_MAX_LEN


def test_merge_tags_earlier_list_takes_priority():
    result = ContentGenerator.merge_tags(
        ["first", "second"],
        ["third", "fourth"],
    )
    assert result[0] == "first"
    assert result[1] == "second"


def test_merge_tags_empty_inputs():
    assert ContentGenerator.merge_tags([], []) == []


def test_merge_tags_skips_blank_tags():
    result = ContentGenerator.merge_tags(["planner", "  ", "digital"])
    assert "  " not in result
    assert "" not in result
