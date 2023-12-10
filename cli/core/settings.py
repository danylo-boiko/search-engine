from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_TITLE: str = "Search engine CLI"
    DEFAULT_CRAWLER_URL: str = "https://en.wikipedia.org"
    DEFAULT_THREADS_COUNT: int = 4


settings = Settings()
