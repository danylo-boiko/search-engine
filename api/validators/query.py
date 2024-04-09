from fastapi import HTTPException

from api.settings import settings
from common.utils import remove_punctuation


def query_validator(query: str) -> str:
    unique_words = set([word for word in remove_punctuation(query).split() if word.isalpha()])

    if len(unique_words) < settings.min_unique_words_count_in_query:
        message = f"Query must contain at least {settings.min_unique_words_count_in_query} unique words"
        raise HTTPException(status_code=400, detail=message)

    return query
