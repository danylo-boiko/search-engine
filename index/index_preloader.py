from sentence_transformers import SentenceTransformer

from index import Index
from index.core import settings
from localization.enums import Language


class IndexPreloader:
    def __init__(self, preload_all: bool = True) -> None:
        self.model = SentenceTransformer(settings.SENTENCE_TRANSFORMER_MODEL)
        self.indexes = {}

        if not preload_all:
            return

        for language in [Language(value) for value in Language]:
            self.indexes[language] = Index(language, self.model)

    def get_index(self, language: Language) -> Index:
        if language not in self.indexes:
            self.indexes[language] = Index(language, self.model)

        return self.indexes[language]
