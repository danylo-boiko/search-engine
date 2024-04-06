from pydantic_settings import BaseSettings

from common.enums import Language


class Settings(BaseSettings):
    SUPPORTED_LANGUAGES: set[Language] = {Language.ENGLISH, Language.UKRAINIAN}
    DB_NAME: str
    DB_CONNECTION_STRING: str


settings = Settings(_env_file=".env")
