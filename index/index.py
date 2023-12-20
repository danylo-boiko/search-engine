from hashlib import md5
from logging import warning
from time import time

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, PyMongoError

from index.core import settings
from localization.enums import Language


class Index:
    def __init__(self, language: Language) -> None:
        client = MongoClient(settings.MONGO_CONNECTION_STRING)
        database = client.get_database(settings.SEARCH_INDEX_DB)

        self.collection = database.get_collection(f"{language}_documents")
        self.__setup_indexes()

    def add_document(self, title: str, url: str, content: str) -> bool:
        try:
            self.collection.insert_one({
                "title": title,
                "url": url,
                "content": content,
                "content_hash": self.__compute_content_hash(content),
                "created_at": time()
            })
            return True
        except PyMongoError as error:
            if not isinstance(error, DuplicateKeyError):
                warning(f"Creating index for url {url} failed")
            return False

    def __setup_indexes(self) -> None:
        self.collection.create_index("content_hash", unique=True)

    def __compute_content_hash(self, content: str) -> str:
        return md5(content.encode()).hexdigest()
