from mongoengine import connect, disconnect
from scrapy import Spider

from crawler.src.items import CrawledPage
from modules.common import settings
from modules.index.services import IndexService


class IndexPipeline:
    def __init__(self) -> None:
        connect(settings.MONGO_DB_NAME, host=settings.MONGO_CONNECTION_STRING)
        self.index_service = IndexService()

    def __del__(self) -> None:
        disconnect()

    def process_item(self, page: CrawledPage, _: Spider) -> CrawledPage:
        self.index_service.index_crawled_page(page.title, page.url, page.language, page.content_items)
        return page