from pydantic import BaseModel

from localization.enums import Language


class ContentResource(BaseModel):
    title: str
    url: str


class SearchResult(BaseModel):
    id: str
    query: str
    summary: str
    resources: list[ContentResource]
    language: Language
    createdAt: float
    timeTaken: float
