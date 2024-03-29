from lingua import LanguageDetectorBuilder

from modules.common.enums import Language
from modules.common import settings


class LanguageDetectionService:
    def __init__(self) -> None:
        supported_lingua_languages = [language.to_lingua_language() for language in settings.SUPPORTED_LANGUAGES]
        self.lingua_detector = LanguageDetectorBuilder.from_languages(*supported_lingua_languages).build()

    def detect(self, text: str) -> Language | None:
        detected_language = self.lingua_detector.detect_language_of(text)

        if not detected_language:
            return None

        return Language.from_lingua_language(detected_language)
