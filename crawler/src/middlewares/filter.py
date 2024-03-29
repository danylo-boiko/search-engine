from typing import Iterator

from scrapy import Request, Spider
from scrapy.http import Response

from crawler.src.items import CrawledPage
from crawler.src.settings import MIN_WORDS_IN_CONTENT_ITEM
from modules.common.utils import remove_punctuation_marks


class FilterMiddleware:
    def process_spider_output(
        self,
        response: Response,
        result: Iterator[CrawledPage | Request],
        spider: Spider
    ) -> Iterator[CrawledPage | Request]:
        for item in result:
            if isinstance(item, CrawledPage):
                item.content_items = self._filter_content_items(item.content_items)
                if item.content_items:
                    yield item
            else:
                yield item

    def _filter_content_items(self, content_items: list[str]) -> list[str]:
        filtered_content_items = []

        for content_item in content_items:
            words = [word for word in remove_punctuation_marks(content_item).split() if word.isalpha()]

            if len(words) >= MIN_WORDS_IN_CONTENT_ITEM:
                filtered_content_items.append(content_item)

        return filtered_content_items
