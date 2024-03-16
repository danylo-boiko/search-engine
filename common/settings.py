from pydantic_settings import BaseSettings

from common.enums import Language


class Settings(BaseSettings):
    DEFAULT_LANGUAGE: Language = Language.ENGLISH
    SUPPORTED_LANGUAGES: set[Language] = {Language.ENGLISH, Language.UKRAINIAN}
    EMBEDDING_MODEL_NAME: str = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
    SUMMARIZER_MODEL_NAME: str = "csebuetnlp/mT5_multilingual_XLSum"
    MONGO_SEARCH_ENGINE_DB: str = "search-engine"
    MONGO_CONNECTION_STRING: str


settings = Settings()
