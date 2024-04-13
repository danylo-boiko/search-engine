from sentence_transformers import SentenceTransformer

from common import settings


class EmbeddingService:
    def __init__(self) -> None:
        self._embedding_model = SentenceTransformer(settings.embedding_model_name)

    def encode(self, text: str) -> list[float]:
        return self._embedding_model.encode(text).tolist()

    def encode_range(self, texts: list[str]) -> list[list[float]]:
        return [embedding.tolist() for embedding in self._embedding_model.encode(texts)]
