from time import time
from uuid import uuid4

from fastapi import APIRouter

from api.schemas import SearchResult
from common.settings import settings
from localization import LanguageDetector
from localization.enums import Language


router = APIRouter()
language_detector = LanguageDetector(settings.SUPPORTED_LANGUAGES)


@router.get("/", response_model=SearchResult)
def search(query: str, preferred_language: Language | None = None) -> SearchResult:
    start_time = time()

    language = language_detector.detect(query)

    if not language:
        language = preferred_language or settings.DEFAULT_LANGUAGE

    end_time = time()

    return SearchResult(
        id=str(uuid4()),
        query=query,
        summaries=[],
        language=language,
        createdAt=end_time,
        timeTaken=end_time - start_time
    )
