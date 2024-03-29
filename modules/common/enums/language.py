from enum import StrEnum

from lingua import Language as LinguaLanguage


class Language(StrEnum):
    ENGLISH = "en"
    UKRAINIAN = "uk"

    @classmethod
    def from_lingua_language(cls, language: LinguaLanguage) -> "Language":
        iso_code = language.iso_code_639_1.name.lower()
        return Language(iso_code)

    def to_lingua_language(self) -> LinguaLanguage:
        for language in LinguaLanguage.all():
            if language.name == self.name:
                return language

        raise ValueError(f"{self.name} is not supported by lingua")
