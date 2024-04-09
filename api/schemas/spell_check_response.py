from pydantic import BaseModel


class SpellCheckResponse(BaseModel):
    is_valid: bool
    autocorrected_query: str | None = None
