from pydantic_settings import BaseSettings

from common.enums import Language


class Settings(BaseSettings):
    DEFAULT_LANGUAGE: Language = Language.ENGLISH
    SUPPORTED_LANGUAGES: set[Language] = {Language.ENGLISH, Language.UKRAINIAN}
    MONGO_SEARCH_ENGINE_DB: str = "search-engine"
    MONGO_CONNECTION_STRING: str


settings = Settings()
