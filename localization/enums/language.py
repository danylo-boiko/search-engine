from enum import StrEnum

from lingua import Language as LinguaLanguage


class Language(StrEnum):
    ENGLISH = "en"
    UKRAINIAN = "uk"

    @classmethod
    def from_lingua_language(cls, language: LinguaLanguage):
        if language == LinguaLanguage.ENGLISH:
            return cls.ENGLISH
        elif language == LinguaLanguage.UKRAINIAN:
            return cls.UKRAINIAN

        raise NotImplementedError(f"{language} is not supported")
