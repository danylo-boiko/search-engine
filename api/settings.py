from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_TITLE: str = "Search engine API"
    V1_PREFIX: str = "/api/v1"
    MIN_UNIQUE_WORDS_COUNT_IN_QUERY: int = 3


settings = Settings()
