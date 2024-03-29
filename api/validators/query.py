from fastapi import HTTPException

from api.settings import settings
from modules.common.utils import remove_punctuation_marks


def query_validator(query: str) -> str:
    unique_words = set([word for word in remove_punctuation_marks(query).split() if word.isalpha()])

    if len(unique_words) < settings.MIN_UNIQUE_WORDS_COUNT_IN_QUERY:
        raise HTTPException(
            status_code=400,
            detail=f"Query must contain at least {settings.MIN_UNIQUE_WORDS_COUNT_IN_QUERY} unique words"
        )

    return query
