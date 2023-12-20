from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    CLI_PROJECT_TITLE: str = "Search engine CLI"
    DEFAULT_THREADS_COUNT: int = 4


settings = Settings()
