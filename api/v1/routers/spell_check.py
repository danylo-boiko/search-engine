from fastapi import APIRouter, Depends, HTTPException, Request

from api.schemas import SpellCheckResponse
from api.services import SpellCheckService, LanguageDetectionService
from api.v1.dependencies import get_language_detection_service, get_spell_check_service
from api.validators import query_validator
from common import settings
from common.enums import Language


router = APIRouter()


@router.get("", response_model=SpellCheckResponse)
def spell_check(
    request: Request,
    query: str = Depends(query_validator),
    language_detection_service: LanguageDetectionService = Depends(get_language_detection_service),
    spell_check_service: SpellCheckService = Depends(get_spell_check_service)
) -> SpellCheckResponse:
    language = language_detection_service.detect(query, request.client.host)

    if language not in settings.supported_languages_lingua:
        raise HTTPException(status_code=400, detail=f"{language.name.capitalize()} language is not supported")

    autocorrected_query = spell_check_service.autocorrect(query, Language.from_lingua_language(language))

    if query == autocorrected_query:
        return SpellCheckResponse(is_valid=True)

    return SpellCheckResponse(is_valid=False, autocorrected_query=autocorrected_query)
