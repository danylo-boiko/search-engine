from scrapy import Spider

from indexer.models import CrawledPage
from indexer.indexer import Indexer


class IndexerPipeline:
    def open_spider(self, spider: Spider) -> None:
        self.indexer = Indexer()

    def close_spider(self, spider: Spider) -> None:
        del self.indexer

    def process_item(self, page: CrawledPage, spider: Spider) -> CrawledPage:
        self.indexer.add_page(getattr(spider, "language"), page)
        return page
