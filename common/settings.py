from pydantic_settings import BaseSettings

from localization.enums import Language


class Settings(BaseSettings):
    DEFAULT_LANGUAGE: Language = Language.ENGLISH
    SUPPORTED_LANGUAGES: set[Language] = {Language.ENGLISH, Language.UKRAINIAN}
    MIN_WORDS_PER_CONTENT_ITEM: int = 8
    MONGO_SEARCH_ENGINE_DB: str = "search-engine"
    MONGO_CONNECTION_STRING: str


settings = Settings()
