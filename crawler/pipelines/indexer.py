from scrapy import Spider

from common import settings
from indexer.models import CrawledPage
from indexer.indexer import Indexer


class IndexerPipeline:
    def open_spider(self, spider: Spider) -> None:
        self.indexer = Indexer(settings.MONGO_CONNECTION_STRING, settings.MONGO_SEARCH_ENGINE_DB, settings.SUPPORTED_LANGUAGES)

    def close_spider(self, spider: Spider) -> None:
        del self.indexer

    def process_item(self, page: CrawledPage, spider: Spider) -> CrawledPage:
        self.indexer.add_page(page, getattr(spider, "language"))
        return page
