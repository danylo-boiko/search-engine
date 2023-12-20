from lingua import LanguageDetectorBuilder
from lingua import Language as LinguaLanguage

from localization.enums import Language


class LanguageDetector:
    def __init__(self) -> None:
        self.supported_languages = {LinguaLanguage.ENGLISH, LinguaLanguage.UKRAINIAN}
        self.lingua_detector = LanguageDetectorBuilder.from_languages(*self.supported_languages).build()

    def detect(self, text: str) -> Language | None:
        detected_language = self.lingua_detector.detect_language_of(text)

        if not detected_language:
            return None

        return Language.from_lingua_language(detected_language)


language_detector = LanguageDetector()
