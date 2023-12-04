from lingua import Language


class Config:
    DEFAULT_LANGUAGE: Language = Language.ENGLISH
    SUPPORTED_LANGUAGES: set[Language] = {Language.ENGLISH, Language.UKRAINIAN}


config = Config()
