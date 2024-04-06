from dataclasses import dataclass

from common.enums import Language


@dataclass
class CrawledPage:
    title: str
    url: str
    language: Language
    content_items: list[str]
