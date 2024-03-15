import logging

from time import time

from pymongo import MongoClient
from pymongo.errors import PyMongoError, DuplicateKeyError
from sentence_transformers import SentenceTransformer

from common import settings
from indexer.models import CrawledPage, PageSummary
from common.enums import Language


class Indexer:
    def __init__(self) -> None:
        self.client = MongoClient(settings.MONGO_CONNECTION_STRING)
        self.database = self.client.get_database(settings.MONGO_SEARCH_ENGINE_DB)

        self.pages_collections = {}
        self.content_items_collections = {}

        for language in settings.SUPPORTED_LANGUAGES:
            self.pages_collections[language] = self.database.get_collection(f"{language}_pages")
            self.pages_collections[language].create_index("content_hash", unique=True)

            self.content_items_collections[language] = self.database.get_collection(f"{language}_content_items")

        self.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME)

    def __del__(self) -> None:
        self.client.close()

    def find_pages(self, query: str, language: Language) -> list[PageSummary]:
        return []

    def add_page(self, page: CrawledPage, language: Language) -> None:
        try:
            inserted_page = self.pages_collections[language].insert_one({
                "title": page.title,
                "url": page.url,
                "content_hash": page.content_items_hash,
                "created_at": time()
            })

            self.content_items_collections[language].insert_many([{
                "page_id": inserted_page.inserted_id,
                "content": content_item
            } for content_item in page.content_items])

            logging.info(f"Inserted page {inserted_page.inserted_id} {page.title}")
        except PyMongoError as error:
            if not isinstance(error, DuplicateKeyError):
                logging.error(error)
