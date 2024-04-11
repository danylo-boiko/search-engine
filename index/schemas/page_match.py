from dataclasses import dataclass


@dataclass
class ContentMatch:
    content: str
    score: float


@dataclass
class PageMatch:
    title: str
    url: str
    content_matches: list[ContentMatch]
