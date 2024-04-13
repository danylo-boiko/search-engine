from dataclasses import dataclass


@dataclass
class CrawledPage:
    title: str
    url: str
    content_items: list[str]

    def __init__(self, title: str, url: str, content_items: list[str]) -> None:
        self.title = title
        self.url = url
        self.content_items = content_items
