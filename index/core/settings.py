from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGO_CONNECTION_STRING: str
    SEARCH_INDEX_DB: str


settings = Settings()
