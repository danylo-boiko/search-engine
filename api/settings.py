from pydantic import Extra
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    project_title: str = "Search engine API"
    v1_prefix: str = "/api/v1"
    min_unique_words_count_in_query: int = 3

    class Config:
        extra = Extra.allow


settings = Settings(_env_file=".env")
