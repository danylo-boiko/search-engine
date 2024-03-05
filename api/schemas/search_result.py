from pydantic import BaseModel

from localization.enums import Language


class PageSummary(BaseModel):
    title: str
    url: str
    summary: str


class SearchResult(BaseModel):
    id: str
    query: str
    summaries: list[PageSummary]
    language: Language
    createdAt: float
    timeTaken: float
