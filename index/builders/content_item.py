from common.enums import Language
from index.models import Page, ContentItem


class ContentItemBuilder:
    def __init__(self) -> None:
        self._page = None
        self._content = None
        self._language = None

    def with_page(self, page: Page) -> "ContentItemBuilder":
        self._page = page
        return self

    def with_content(self, content: str) -> "ContentItemBuilder":
        self._content = content
        return self

    def with_language(self, language: Language) -> "ContentItemBuilder":
        self._language = language
        return self

    def build(self) -> ContentItem:
        if not self._page:
            raise ValueError("Page is required")

        if not self._content:
            raise ValueError("Content is required")

        if not self._language:
            raise ValueError("Language is required")

        content_item = ContentItem(
            page=self._page,
            content=self._content,
            language=self._language
        )

        content_item.validate()

        return content_item
