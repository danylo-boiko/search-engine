from lingua import LanguageDetectorBuilder

from localization.enums import Language


class LanguageDetector:
    def __init__(self, supported_languages: list[Language]) -> None:
        lingua_languages = [language.to_lingua_language() for language in supported_languages]
        self.lingua_detector = LanguageDetectorBuilder.from_languages(*lingua_languages).build()

    def detect(self, text: str) -> Language | None:
        detected_language = self.lingua_detector.detect_language_of(text)

        if not detected_language:
            return None

        return Language.from_lingua_language(detected_language)
