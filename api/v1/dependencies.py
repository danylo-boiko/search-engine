from api.services import SpellCheckService, LanguageDetectionService
from modules.index.services import IndexService


spell_check_service = SpellCheckService()
language_detection_service = LanguageDetectionService()
index_service = IndexService()


def get_spell_check_service() -> SpellCheckService:
    return spell_check_service


def get_language_detection_service() -> LanguageDetectionService:
    return language_detection_service


def get_index_service() -> IndexService:
    return index_service
