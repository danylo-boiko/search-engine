from fastapi import HTTPException

from api.settings import settings


punctuation_marks = set("!\"#$%&()*+,/:;<=>?@[\\]^_`{|}~.")


def query_validator(query: str) -> str:
    filtered_query = "".join([char for char in query if char not in punctuation_marks])

    unique_words = set([word for word in filtered_query.split() if word.isalpha()])

    if len(unique_words) < settings.MIN_UNIQUE_WORDS_COUNT_IN_QUERY:
        raise HTTPException(
            status_code=400,
            detail=f"Query must contain at least {settings.MIN_UNIQUE_WORDS_COUNT_IN_QUERY} unique words"
        )

    return query
