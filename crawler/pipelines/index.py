from mongoengine import connect, disconnect
from scrapy import Spider

from common import settings
from crawler.items import CrawledPage
from index.services import IndexService


class IndexPipeline:
    def __init__(self) -> None:
        connect(settings.db_name, host=settings.db_connection_string)
        self.index_service = IndexService()

    def __del__(self) -> None:
        disconnect()

    def process_item(self, page: CrawledPage, _: Spider) -> CrawledPage:
        self.index_service.index_page(page.title, page.url, page.content_items)
        return page
