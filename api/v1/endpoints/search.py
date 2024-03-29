from time import time
from uuid import uuid4

from fastapi import APIRouter, Depends

from api.schemas import SearchResult
from api.services import LanguageDetectionService
from api.v1.dependencies import get_language_detection_service, get_index_service
from api.validators import query_validator
from modules.index.services import IndexService


router = APIRouter()


@router.get("", response_model=SearchResult)
def search(
    query: str = Depends(query_validator),
    language_detection_service: LanguageDetectionService = Depends(get_language_detection_service),
    index_service: IndexService = Depends(get_index_service)
) -> SearchResult:
    start_time = time()

    language = language_detection_service.detect(query)

    pages = index_service.find_indexed_pages(query, language)

    end_time = time()

    return SearchResult(
        id=uuid4(),
        query=query,
        language=language,
        pages=pages,
        createdAt=end_time,
        timeTaken=end_time - start_time
    )
