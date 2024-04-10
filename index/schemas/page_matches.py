from dataclasses import dataclass


@dataclass
class ContentMatch:
    content: str
    score: float


@dataclass
class PageMatches:
    title: str
    url: str
    content_matches: list[ContentMatch]
