from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, Depends

from api.schemas import SearchResult
from api.services import LanguageDetectionService
from api.v1.dependencies import get_language_detection_service
from api.validators import query_validator


router = APIRouter()


@router.get("", response_model=SearchResult)
def search(
    query: str = Depends(query_validator),
    language_detection_service: LanguageDetectionService = Depends(get_language_detection_service)
) -> SearchResult:
    start_time = datetime.utcnow()

    language = language_detection_service.detect(query)

    end_time = datetime.utcnow()

    return SearchResult(
        id=uuid4(),
        query=query,
        language=language,
        pages=[],
        createdAt=end_time,
        timeTaken=(end_time - start_time).microseconds // 1000
    )
