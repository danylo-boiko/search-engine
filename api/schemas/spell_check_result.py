from pydantic import BaseModel


class SpellCheckResult(BaseModel):
    is_valid: bool
    autocorrected_query: str | None
