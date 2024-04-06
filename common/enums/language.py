from enum import StrEnum

from lingua import Language as LinguaLanguage


class Language(StrEnum):
    ENGLISH = "en"
    UKRAINIAN = "uk"

    @classmethod
    def from_lingua_language(cls, language: LinguaLanguage) -> "Language":
        return cls(language.iso_code_639_1.name.lower())

    def to_lingua_language(self) -> LinguaLanguage:
        return next(language for language in LinguaLanguage.all() if language.name == self.name)
