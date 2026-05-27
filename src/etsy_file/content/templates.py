from dataclasses import dataclass, field


@dataclass
class RenderedContent:
    title: str
    description: str
    tags: list[str]


@dataclass
class ListingTemplate:
    """
    A reusable template for an Etsy listing.

    title_template and description_template use str.format() syntax:
        "Daily Planner {year} | {format} Download"
    Tags may also contain {var} placeholders.
    """

    name: str
    title_template: str
    description_template: str
    base_tags: list[str] = field(default_factory=list)

    def render(self, variables: dict) -> RenderedContent:
        """Substitute *variables* into all template fields."""
        title = self.title_template.format(**variables)
        description = self.description_template.format(**variables)
        tags = [t.format(**variables) for t in self.base_tags]
        return RenderedContent(title=title, description=description, tags=tags)
