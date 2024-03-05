import logging

from time import time

from pymongo import MongoClient
from pymongo.errors import PyMongoError, DuplicateKeyError

from indexer.models import CrawledPage, PageSummary
from localization.enums import Language


class Indexer:
    def __init__(self, connection_string: str, search_engine_db: str, supported_languages: list[Language]) -> None:
        self.client = MongoClient(connection_string)
        self.database = self.client.get_database(search_engine_db)

        self.pages_collections = {}
        self.content_items_collections = {}

        for language in supported_languages:
            self.pages_collections[language] = self.database.get_collection(f"{language}_pages")
            self.pages_collections[language].create_index("content_hash", unique=True)

            self.content_items_collections[language] = self.database.get_collection(f"{language}_content_items")

    def __del__(self) -> None:
        self.client.close()

    def find_pages(self, query: str, language: Language) -> list[PageSummary]:
        return []

    def add_page(self, page: CrawledPage, language: Language) -> None:
        try:
            inserted_page = self.pages_collections[language].insert_one({
                "title": page.title,
                "url": page.url,
                "content_hash": page.get_content_items_hash(),
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
