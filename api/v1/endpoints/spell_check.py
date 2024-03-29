from fastapi import APIRouter, Depends

from api.schemas import SpellCheckResult
from api.services import LanguageDetectionService, SpellCheckService
from api.v1.dependencies import get_spell_check_service, get_language_detection_service
from api.validators import query_validator


router = APIRouter()


@router.get("", response_model=SpellCheckResult)
def spell_check(
    query: str = Depends(query_validator),
    language_detection_service: LanguageDetectionService = Depends(get_language_detection_service),
    spell_check_service: SpellCheckService = Depends(get_spell_check_service)
) -> SpellCheckResult:
    detected_language = language_detection_service.detect(query)

    autocorrected_query = spell_check_service.autocorrect(query, detected_language)

    return SpellCheckResult(
        is_valid=query == autocorrected_query,
        autocorrected_query=autocorrected_query if query != autocorrected_query else None
    )
