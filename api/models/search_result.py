from dataclasses import dataclass
from uuid import UUID

from indexer.models import PageSummary
from common.enums import Language


@dataclass
class SearchResult:
    id: UUID
    query: str
    language: Language
    pages: list[PageSummary]
    createdAt: float
    timeTaken: float
