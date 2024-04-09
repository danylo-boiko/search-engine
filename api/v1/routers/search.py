from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Request

from api.schemas import SearchResponse, PageSummary
from api.services import LanguageDetectionService
from api.v1.dependencies import get_language_detection_service, get_index_service
from api.validators import query_validator
from common import settings
from common.enums import Language
from index.services import IndexService


router = APIRouter()


@router.get("", response_model=SearchResponse)
def search(
    request: Request,
    query: str = Depends(query_validator),
    language_detection_service: LanguageDetectionService = Depends(get_language_detection_service),
    index_service: IndexService = Depends(get_index_service)
) -> SearchResponse:
    start_time = datetime.utcnow()

    language = language_detection_service.detect(query, request.client.host)

    if language not in settings.supported_languages_lingua:
        raise HTTPException(status_code=400, detail=f"{language.name.capitalize()} language is not supported")

    pages = index_service.find_pages(query, Language.from_lingua_language(language))

    end_time = datetime.utcnow()

    return SearchResponse(
        id=uuid4(),
        query=query,
        language=Language.from_lingua_language(language),
        pages=[
            PageSummary(
                title=page.title,
                url=page.url,
                summary=" ".join(content_item.content for content_item in page.content_items)
            ) for page in pages
        ],
        created_at=end_time,
        time_taken=(end_time - start_time).microseconds // 1000
    )
