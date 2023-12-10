from lingua import LanguageDetectorBuilder

from localization.core import settings
from localization.enums import Language


class LanguageDetector:
    def __init__(self) -> None:
        self.lingua_detector = LanguageDetectorBuilder.from_languages(*settings.SUPPORTED_LANGUAGES).build()

    def detect(self, text: str, preferred_language: Language | None = None) -> Language:
        detected_language = self.lingua_detector.detect_language_of(text)

        if not detected_language:
            if preferred_language:
                return preferred_language

            detected_language = settings.DEFAULT_LANGUAGE

        return Language.from_lingua_language(detected_language)


language_detector = LanguageDetector()
