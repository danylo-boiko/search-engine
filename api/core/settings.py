from pydantic_settings import BaseSettings

from localization.enums import Language


class Settings(BaseSettings):
    PROJECT_TITLE: str = "Search engine API"
    DEFAULT_LANGUAGE: Language = Language.ENGLISH
    API_V1_PREFIX: str = "/api/v1"
    CORS_ORIGINS: set[str] = {"http://localhost:4200"}


settings = Settings()
