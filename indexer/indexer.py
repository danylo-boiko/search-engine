import logging
from time import time

from sentence_transformers import SentenceTransformer

from common import settings
from indexer.models import CrawledPage, PageSummary
from common.enums import Language
from indexer.repositories import MongoRepository


class Indexer:
    def __init__(self) -> None:
        self.repository = MongoRepository()
        self.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME)

    def __del__(self) -> None:
        del self.repository

    def find_pages(self, query: str, language: Language) -> list[PageSummary]:
        return [PageSummary(
            title=page["title"],
            url=page["url"],
            summary=" ".join(page["content_items"])
        ) for page in self.repository.find_by_content_embedding(language, self.__get_embedding(query))]

    def add_page(self, page: CrawledPage, language: Language) -> None:
        page_id = self.repository.add_page(language, {
            "title": page.title,
            "url": page.url,
            "content_hash": page.content_items_hash,
            "created_at": time()
        })

        if not page_id:
            return

        self.repository.add_content_items(language, [{
            "page_id": page_id,
            "content": content_item,
            "content_embedding": self.__get_embedding(content_item)
        } for content_item in page.content_items])

        logging.info(f"Inserted page {page_id} {page.title}")

    def __get_embedding(self, text: str) -> list[float]:
        return self.embedding_model.encode(text).tolist()
