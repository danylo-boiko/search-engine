from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGO_CONNECTION_STRING: str
    SEARCH_INDEX_DB: str
    SENTENCE_TRANSFORMER_MODEL: str = "sentence-transformers/all-mpnet-base-v2"


settings = Settings()
