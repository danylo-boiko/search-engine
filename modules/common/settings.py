from pydantic_settings import BaseSettings

from modules.common.enums import Language


class Settings(BaseSettings):
    DEFAULT_LANGUAGE: Language = Language.ENGLISH
    SUPPORTED_LANGUAGES: set[Language] = {Language.ENGLISH, Language.UKRAINIAN}
    MONGO_CONNECTION_STRING: str


settings = Settings()
