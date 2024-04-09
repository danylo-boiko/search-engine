from datetime import datetime
from hashlib import md5

from index.models import Page


class PageBuilder:
    def __init__(self) -> None:
        self._title = None
        self._url = None
        self._content_items = None

    def with_title(self, title: str) -> "PageBuilder":
        self._title = title
        return self

    def with_url(self, url: str) -> "PageBuilder":
        self._url = url
        return self

    def with_content_items(self, content_items: list[str]) -> "PageBuilder":
        self._content_items = content_items
        return self

    def build(self) -> Page:
        if not self._title:
            raise ValueError("Title is required")

        if not self._url:
            raise ValueError("Url is required")

        if not self._content_items:
            raise ValueError("Content items are required")

        return Page(
            title=self._title,
            url=self._url,
            content_hash=self._compute_content_hash(),
            created_at=datetime.utcnow()
        )

    def _compute_content_hash(self) -> str:
        encoded_content = "".join(self._content_items).encode()
        return md5(encoded_content).hexdigest()
