from babel.languages import get_territory_language_info
from geocoder import ip
from lingua import LanguageDetectorBuilder, Language


class LanguageDetectionService:
    def __init__(self) -> None:
        self._lingua_detector = LanguageDetectorBuilder.from_all_languages().with_preloaded_language_models().build()

    def detect(self, text: str, host: str) -> Language | None:
        country_code = ip(host).country

        territory_language_info = get_territory_language_info(country_code)

        if not territory_language_info:
            return self._lingua_detector.detect_language_of(text)

        language_confidence_map = {}

        for language_confidence in self._lingua_detector.compute_language_confidence_values(text):
            language_info = territory_language_info.get(language_confidence.language.iso_code_639_1.name.lower())
            confidence = language_confidence.value

            if language_info:
                if language_info["official_status"] == "official":
                    confidence *= 1.25
                elif language_info["official_status"] == "de_facto_official":
                    confidence *= 1.1

                confidence *= 1 + (language_info["population_percent"] * 0.0025)

            language_confidence_map[language_confidence.language] = confidence

        return max(language_confidence_map, key=language_confidence_map.get)
