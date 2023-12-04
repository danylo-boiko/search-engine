from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_TITLE: str = "Search engine"
    API_V1_PREFIX: str = "/api/v1"
    CORS_ORIGINS: set[str] = set()


settings = Settings()
