from typing import Iterator

from scrapy import Spider, Request
from scrapy.http import Response

from crawler.settings import MIN_WORDS_IN_CONTENT_ITEM
from indexer.models import CrawledPage


class FilterMiddleware:
    def process_spider_output(self, response: Response, result: Iterator[CrawledPage | Request], spider: Spider) -> Iterator[CrawledPage | Request]:
        for item in result:
            if isinstance(item, CrawledPage):
                item.content_items = [
                    content_item for content_item in item.content_items
                    if len(content_item.split()) >= MIN_WORDS_IN_CONTENT_ITEM
                ]

                if item.content_items:
                    yield item
            else:
                yield item
