from hashlib import md5
from logging import warning
from time import time

from pymongo import MongoClient
from pymongo.command_cursor import CommandCursor
from pymongo.errors import DuplicateKeyError, PyMongoError
from sentence_transformers import SentenceTransformer

from index.core import settings
from localization.enums import Language


class Index:
    def __init__(self, language: Language, model: SentenceTransformer | None = None) -> None:
        self.language = language
        self.model = model if model else SentenceTransformer(settings.SENTENCE_TRANSFORMER_MODEL)

        client = MongoClient(settings.MONGO_CONNECTION_STRING)
        database = client.get_database(settings.SEARCH_INDEX_DB)

        self.pages_collection = database.get_collection(f"{self.language}_pages")
        self.pages_collection.create_index("content_hash", unique=True)

        self.content_items_collection = database.get_collection(f"{self.language}_content_items")

    def find_pages(self, query: str, top_k: int = 5) -> CommandCursor:
        return self.content_items_collection.aggregate([
            {
                "$vectorSearch": {
                    "index": "default",
                    "path": "embedding",
                    "queryVector": self.model.encode(query).tolist(),
                    "numCandidates": top_k * 10,
                    "limit": top_k
                }
            }, {
                "$group": {
                    "_id": "$page_id",
                    "content_items": {"$push": "$content"}
                }
            }, {
                "$lookup": {
                    "from": f"{self.language}_pages",
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

    def add_page(self, title: str, url: str, content_items: list[str]) -> bool:
        try:
            inserted_page = self.pages_collection.insert_one({
                "title": title,
                "url": url,
                "content_hash": self.__compute_hash(" ".join(content_items)),
                "created_at": time()
            })

            if len(content_items) > 0:
                self.content_items_collection.insert_many([{
                    "page_id": inserted_page.inserted_id,
                    "content": content_item,
                    "embedding": self.model.encode(content_item).tolist()
                } for content_item in content_items])

            return True
        except PyMongoError as error:
            if not isinstance(error, DuplicateKeyError):
                warning(f"Creating index for url {url} failed")
            return False

    def __compute_hash(self, text: str) -> str:
        return md5(text.encode()).hexdigest()
