from lingua import Language as LinguaLanguage
from pydantic_settings import BaseSettings

from common.enums import Language


class Settings(BaseSettings):
    supported_languages: set[Language] = {Language.ENGLISH, Language.UKRAINIAN}
    db_name: str
    db_connection_string: str

    @property
    def supported_languages_lingua(self) -> set[LinguaLanguage]:
        return set(language.to_lingua_language() for language in self.supported_languages)


settings = Settings(_env_file=".env")
