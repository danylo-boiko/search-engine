from typing import Iterator

from scrapy import Spider, Request
from scrapy.http import Response

from common.settings import settings
from crawler.items import CrawledItem


class CrawlerSpiderMiddleware:
    def process_spider_output(self, response: Response, result: Iterator[CrawledItem | Request], spider: Spider) -> Iterator[CrawledItem | Request]:
        for item in result:
            if isinstance(item, CrawledItem):
                item.content_items = [
                    content_item for content_item in item.content_items
                    if len(content_item.split()) >= settings.MIN_WORDS_PER_CONTENT_ITEM
                ]

                if item.content_items:
                    yield item
            else:
                yield item
