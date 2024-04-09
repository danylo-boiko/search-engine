from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from common.enums import Language


class PageSummary(BaseModel):
    title: str
    url: str
    summary: str


class SearchResponse(BaseModel):
    id: UUID
    query: str
    language: Language
    pages: list[PageSummary]
    created_at: datetime
    time_taken: int
