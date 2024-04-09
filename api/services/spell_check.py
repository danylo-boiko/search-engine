from autocorrect import Speller

from common import settings
from common.enums import Language


class SpellCheckService:
    def __init__(self) -> None:
        self._spellers = {language: Speller(language) for language in settings.supported_languages}

    def autocorrect(self, text: str, language: Language) -> str:
        return self._spellers[language].autocorrect_sentence(text)
