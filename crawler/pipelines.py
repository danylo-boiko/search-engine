from time import time

from pymongo import MongoClient
from pymongo.errors import PyMongoError, DuplicateKeyError
from scrapy import Spider

from common.settings import settings
from crawler.items import CrawledItem


class CrawlerPipeline:
    def open_spider(self, spider: Spider) -> None:
        self.client = MongoClient(settings.MONGO_CONNECTION_STRING)
        self.database = self.client.get_database(settings.MONGO_SEARCH_ENGINE_DB)

        language = getattr(spider, "language")

        self.pages_collection = self.database.get_collection(f"{language}_pages")
        self.content_items_collection = self.database.get_collection(f"{language}_content_items")

        self.pages_collection.create_index("content_hash", unique=True)

    def close_spider(self, spider: Spider) -> None:
        self.client.close()

    def process_item(self, item: CrawledItem, spider: Spider) -> CrawledItem:
        try:
            inserted_page = self.pages_collection.insert_one({
                "title": item.title,
                "url": item.url,
                "content_hash": item.compute_content_hash(),
                "created_at": time()
            })

            self.content_items_collection.insert_many([{
                "page_id": inserted_page.inserted_id,
                "content": content_item
            } for content_item in item.content_items])
        except PyMongoError as error:
            if not isinstance(error, DuplicateKeyError):
                spider.logger.error(error)

        return item
