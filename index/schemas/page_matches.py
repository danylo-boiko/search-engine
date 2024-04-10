from dataclasses import dataclass


@dataclass
class ContentMatching:
    content: str
    score: float


@dataclass
class PageMatches:
    title: str
    url: str
    content_items: list[ContentMatching]
