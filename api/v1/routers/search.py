from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Request

from api.schemas import SearchResponse
from api.services import LanguageDetectionService
from api.v1.dependencies import get_language_detection_service
from api.validators import query_validator
from common import settings
from common.enums import Language


router = APIRouter()


@router.get("", response_model=SearchResponse)
def search(
    request: Request,
    query: str = Depends(query_validator),
    language_detection_service: LanguageDetectionService = Depends(get_language_detection_service)
) -> SearchResponse:
    start_time = datetime.utcnow()

    language = language_detection_service.detect(query, request.client.host)

    if language not in settings.supported_languages_lingua:
        raise HTTPException(status_code=400, detail=f"{language.name.capitalize()} language is not supported")

    end_time = datetime.utcnow()

    return SearchResponse(
        id=uuid4(),
        query=query,
        language=Language.from_lingua_language(language),
        pages=[],
        createdAt=end_time,
        timeTaken=(end_time - start_time).microseconds // 1000
    )
