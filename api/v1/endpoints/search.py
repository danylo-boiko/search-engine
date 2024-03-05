from time import time
from uuid import uuid4

from fastapi import APIRouter

from api.models import SearchResult
from common import settings
from indexer import Indexer
from localization import LanguageDetector
from localization.enums import Language


router = APIRouter()
language_detector = LanguageDetector(settings.SUPPORTED_LANGUAGES)
indexer = Indexer(settings.MONGO_CONNECTION_STRING, settings.MONGO_SEARCH_ENGINE_DB, settings.SUPPORTED_LANGUAGES)


@router.get("", response_model=SearchResult)
def search(query: str, preferred_language: Language | None = None) -> SearchResult:
    start_time = time()

    language = language_detector.detect(query)

    if not language:
        language = preferred_language or settings.DEFAULT_LANGUAGE

    pages = indexer.find_pages(query, language)

    end_time = time()

    return SearchResult(
        id=uuid4(),
        query=query,
        language=language,
        pages=pages,
        createdAt=end_time,
        timeTaken=end_time - start_time
    )
