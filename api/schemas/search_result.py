from uuid import UUID

from pydantic import BaseModel

from api.schemas import PageSummary
from modules.common.enums import Language


class SearchResult(BaseModel):
    id: UUID
    query: str
    language: Language
    pages: list[PageSummary]
    createdAt: float
    timeTaken: float
