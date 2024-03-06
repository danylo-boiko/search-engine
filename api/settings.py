from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_PROJECT_TITLE: str = "Search engine API"
    API_V1_PREFIX: str = "/api/v1"
    CORS_ORIGINS: set[str] = {"http://localhost:4200"}


settings = Settings()
