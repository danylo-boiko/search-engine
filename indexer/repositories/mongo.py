import logging

from pymongo import MongoClient
from pymongo.command_cursor import CommandCursor
from pymongo.errors import PyMongoError, DuplicateKeyError

from common import settings
from common.enums import Language


class MongoRepository:
    def __init__(self) -> None:
        self.client = MongoClient(settings.MONGO_CONNECTION_STRING)
        self.database = self.client.get_database(settings.MONGO_SEARCH_ENGINE_DB)

        self.pages_collections = {}
        self.content_items_collections = {}

        for language in settings.SUPPORTED_LANGUAGES:
            self.pages_collections[language] = self.database.get_collection(f"{language}_pages")
            self.pages_collections[language].create_index("content_hash", unique=True)

            self.content_items_collections[language] = self.database.get_collection(f"{language}_content_items")

    def __del__(self) -> None:
        self.client.close()

    def find_by_content_embedding(self, language: Language, embedding: list[float], top_k: int = 5, min_score: float = 0.75) -> CommandCursor:
        return self.content_items_collections[language].aggregate([
            {
                "$vectorSearch": {
                    "index": "content_embedding_index",
                    "path": "content_embedding",
                    "queryVector": embedding,
                    "numCandidates": top_k * 2000,
                    "limit": top_k
                }
            }, {
                "$project": {
                    "_id": 0,
                    "page_id": 1,
                    "content": 1,
                    "score": {"$meta": "vectorSearchScore"}
                }
            }, {
                "$match": {
                    "score": {"$gte": min_score}
                }
            }, {
                "$group": {
                    "_id": "$page_id",
                    "content_items": {"$push": "$content"}
                }
            }, {
                "$lookup": {
                    "from": f"{language}_pages",
                    "localField": "_id",
                    "foreignField": "_id",
                    "as": "page"
                }
            }, {
                "$unwind": "$page"
            }, {
                "$project": {
                    "title": "$page.title",
                    "url": "$page.url",
                    "content_items": 1
                }
            }
        ])

    def add_page(self, language: Language, page: dict[str, any]) -> str | None:
        try:
            return self.pages_collections[language].insert_one(page).inserted_id
        except PyMongoError as error:
            if not isinstance(error, DuplicateKeyError):
                logging.error(error)
            return None

    def add_content_items(self, language: Language, content_items: list[dict[str, any]]) -> None:
        self.content_items_collections[language].insert_many(content_items)
