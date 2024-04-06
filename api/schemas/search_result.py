from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from api.schemas import PageSummary
from common.enums import Language


class SearchResult(BaseModel):
    id: UUID
    query: str
    language: Language
    pages: list[PageSummary]
    createdAt: datetime
    timeTaken: int
