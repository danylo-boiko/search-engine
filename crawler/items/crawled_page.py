from dataclasses import dataclass


@dataclass
class CrawledPage:
    title: str
    url: str
    content_items: list[str]
