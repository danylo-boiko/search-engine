from dataclasses import dataclass


@dataclass
class ContentMatch:
    content: str
    score: float

    def __init__(self, content: str, score: float) -> None:
        self.content = content
        self.score = score


@dataclass
class PageMatch:
    title: str
    url: str
    content_matches: list[ContentMatch]

    def __init__(self, title: str, url: str, content_matches: list[ContentMatch]) -> None:
        self.title = title
        self.url = url
        self.content_matches = content_matches
