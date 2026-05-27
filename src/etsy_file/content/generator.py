from .templates import ListingTemplate, RenderedContent
from .validator import TAG_MAX_COUNT, TAG_MAX_LEN, validate_content


class ContentGenerator:
    def __init__(self, template: ListingTemplate) -> None:
        self._template = template

    def render(self, variables: dict) -> RenderedContent:
        """Render the template and validate the result against Etsy constraints."""
        content = self._template.render(variables)
        validate_content(content.title, content.tags)
        return content

    @staticmethod
    def merge_tags(*tag_lists: list[str]) -> list[str]:
        """
        Merge multiple tag lists into a single deduplicated list.

        Tags are deduplicated case-insensitively, truncated to 20 chars, and
        capped at 13 — matching Etsy's hard limits. Earlier lists take priority.
        """
        seen: set[str] = set()
        result: list[str] = []
        for tags in tag_lists:
            for tag in tags:
                clean = tag[:TAG_MAX_LEN].strip()
                key = clean.lower()
                if key and key not in seen:
                    seen.add(key)
                    result.append(clean)
                    if len(result) == TAG_MAX_COUNT:
                        return result
        return result
