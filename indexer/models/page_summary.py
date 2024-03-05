from dataclasses import dataclass


@dataclass
class PageSummary:
    title: str
    url: str
    summary: str
