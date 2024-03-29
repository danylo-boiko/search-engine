from api.services import SpellCheckService, LanguageDetectionService


spell_check_service = SpellCheckService()
language_detection_service = LanguageDetectionService()


def get_spell_check_service() -> SpellCheckService:
    return spell_check_service


def get_language_detection_service() -> LanguageDetectionService:
    return language_detection_service
