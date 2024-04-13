from babel.languages import get_territory_language_info
from geocoder import ip
from lingua import LanguageDetectorBuilder, Language
from lingua.lingua import ConfidenceValue


class LanguageDetectionService:
    def __init__(self) -> None:
        self._lingua_detector = LanguageDetectorBuilder.from_all_languages().with_preloaded_language_models().build()

    def detect(self, text: str, host: str) -> Language | None:
        host_languages = self._get_host_languages(host)

        if not host_languages:
            return self._lingua_detector.detect_language_of(text)

        language_confidence_map = dict()

        for confidence_value in self._lingua_detector.compute_language_confidence_values(text):
            language_stats = host_languages.get(self._get_confidence_value_language_key(confidence_value))

            confidence = confidence_value.value

            if language_stats:
                confidence *= self._get_confidence_multiplier(language_stats)

            language_confidence_map[confidence_value.language] = confidence

        return max(language_confidence_map, key=language_confidence_map.get)

    def _get_host_languages(self, host: str) -> dict:
        parsed_host = ip(host)
        return get_territory_language_info(parsed_host.country)

    def _get_confidence_value_language_key(self, confidence_value: ConfidenceValue) -> str:
        return confidence_value.language.iso_code_639_1.name.lower()

    def _get_confidence_multiplier(self, language_stats: dict) -> float:
        multiplier = 1 + language_stats["population_percent"] * 0.0025

        if language_stats["official_status"] == "official":
            multiplier += 0.2

        return multiplier
