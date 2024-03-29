from autocorrect import Speller

from modules.common import settings
from modules.common.enums import Language


class SpellCheckService:
    def __init__(self) -> None:
        self._spellers = {language: Speller(language) for language in settings.SUPPORTED_LANGUAGES}

    def autocorrect(self, text: str, language: Language) -> str:
        return self._spellers[language].autocorrect_sentence(text)
