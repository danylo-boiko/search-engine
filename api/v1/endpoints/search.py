from time import time
from uuid import uuid4

from fastapi import APIRouter

from api.core import settings
from api.schemas import SearchResult
from localization import language_detector
from localization.enums import Language

router = APIRouter()


@router.get("/", response_model=SearchResult)
def search(query: str, preferred_language: Language | None = None) -> SearchResult:
    start_time = time()

    language = language_detector.detect(query)

    if not language:
        language = preferred_language if preferred_language else settings.DEFAULT_LANGUAGE

    end_time = time()

    return SearchResult(
        id=str(uuid4()),
        query=query,
        summary="",
        resources=[],
        language=language,
        createdAt=end_time,
        timeTaken=end_time - start_time
    )
