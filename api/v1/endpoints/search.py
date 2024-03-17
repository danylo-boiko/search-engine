from time import time
from uuid import uuid4

from fastapi import APIRouter, HTTPException

from api.localization import LanguageDetector
from api.models import SearchResult
from api.settings import settings as api_settings
from common import settings
from common.enums import Language
from indexer import Indexer


router = APIRouter()
language_detector = LanguageDetector()
indexer = Indexer()


@router.get("", response_model=SearchResult)
def search(query: str, preferred_language: Language | None = None) -> SearchResult:
    if len(set([word for word in query.split() if word.isalpha()])) < api_settings.MIN_UNIQUE_WORDS_IN_QUERY:
        raise HTTPException(400, f"Query must contain at least {api_settings.MIN_UNIQUE_WORDS_IN_QUERY} unique words")

    start_time = time()

    language = language_detector.detect(query)

    if not language:
        language = preferred_language or settings.DEFAULT_LANGUAGE

    pages = indexer.find_pages(language, query)

    end_time = time()

    return SearchResult(
        id=uuid4(),
        query=query,
        language=language,
        pages=pages,
        createdAt=end_time,
        timeTaken=end_time - start_time
    )
