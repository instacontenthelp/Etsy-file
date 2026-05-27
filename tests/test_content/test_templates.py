import pytest

from etsy_file.content.templates import ListingTemplate, RenderedContent


@pytest.fixture
def planner_template():
    return ListingTemplate(
        name="digital-planner",
        title_template="{name} | {year} Printable PDF Planner",
        description_template="Download your {name} for {year}. {details}",
        base_tags=["printable", "{year} planner", "digital download"],
    )


# ------------------------------------------------------------------
# render
# ------------------------------------------------------------------


def test_render_substitutes_title(planner_template):
    content = planner_template.render(
        {"name": "Daily Planner", "year": "2025", "details": "A4 size."}
    )
    assert content.title == "Daily Planner | 2025 Printable PDF Planner"


def test_render_substitutes_description(planner_template):
    content = planner_template.render(
        {"name": "Weekly Planner", "year": "2025", "details": "Letter size."}
    )
    assert "Weekly Planner" in content.description
    assert "2025" in content.description
    assert "Letter size." in content.description


def test_render_substitutes_tags(planner_template):
    content = planner_template.render(
        {"name": "Monthly Planner", "year": "2025", "details": ""}
    )
    assert "2025 planner" in content.tags
    assert "printable" in content.tags


def test_render_returns_rendered_content_instance(planner_template):
    content = planner_template.render(
        {"name": "Budget Planner", "year": "2025", "details": ""}
    )
    assert isinstance(content, RenderedContent)


def test_render_raises_on_missing_variable(planner_template):
    with pytest.raises(KeyError):
        planner_template.render({"name": "Planner"})  # missing year, details


def test_template_with_no_tags_renders_empty_tag_list():
    tmpl = ListingTemplate(
        name="bare",
        title_template="Title",
        description_template="Desc",
        base_tags=[],
    )
    content = tmpl.render({})
    assert content.tags == []
