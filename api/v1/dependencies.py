from api.services import SpellCheckService, LanguageDetectionService
from index.services import SearchService


spell_check_service = SpellCheckService()
language_detection_service = LanguageDetectionService()
search_service = SearchService()


def get_spell_check_service() -> SpellCheckService:
    return spell_check_service


def get_language_detection_service() -> LanguageDetectionService:
    return language_detection_service


def get_search_service() -> SearchService:
    return search_service
