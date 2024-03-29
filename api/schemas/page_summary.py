from pydantic import BaseModel


class PageSummary(BaseModel):
    title: str
    url: str
    summary: str
