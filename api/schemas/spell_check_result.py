from pydantic import BaseModel


class SpellCheckResult(BaseModel):
    is_valid: bool
    fixed_query: str | None
