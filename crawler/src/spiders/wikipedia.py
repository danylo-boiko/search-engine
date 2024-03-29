from re import compile
from typing import Iterable
from urllib.parse import urlparse

from scrapy import Spider, Request
from scrapy.crawler import Crawler
from scrapy.http import Response

from crawler.src.items import CrawledPage
from crawler.src.utils import get_page_title, get_page_urls
from modules.common import settings
from modules.common.enums import Language


class WikipediaSpider(Spider):
    name = "wikipedia"

    def __init__(self, **kwargs: dict[str, str]) -> None:
        super().__init__(self.name)

        start_url, queue = kwargs.get("start_url"), kwargs.get("queue")

        if not start_url and not queue:
            raise RuntimeError("You must specify either 'start_url' or 'queue'")

        if isinstance(start_url, str):
            self.start_urls = [start_url]
            self.queue = urlparse(start_url).netloc
        else:
            self.queue = queue

        self.language = Language(self.queue[:2])

        if self.language not in settings.SUPPORTED_LANGUAGES:
            raise ValueError(f"Language {self.language} is not supported")

        self.allowed_domains = [self.queue]

    def parse(self, response: Response, **kwargs: dict) -> Iterable[CrawledPage | Request]:
        yield CrawledPage(
            title=get_page_title(response),
            url=response.url,
            language=self.language,
            content_items=self.__parse_content_items(response)
        )

        for url in get_page_urls(response):
            yield Request(url, self.parse)

    def _set_crawler(self, crawler: Crawler) -> None:
        super()._set_crawler(crawler)
        self.crawler.settings.set("JOBDIR", f"jobs/{self.queue}")

    def __parse_content_items(self, response: Response) -> list[str]:
        content_items = []

        for paragraph in response.css("div#mw-content-text p"):
            paragraph_items = [item for item in paragraph.css("::text").extract() if not compile(r"\[\d+]").match(item)]

            paragraph_content = "".join(paragraph_items).replace("\n", "").strip()

            if not paragraph_content:
                continue

            if not paragraph_content.endswith("."):
                paragraph_content += "."

            content_items.append(paragraph_content)

        return content_items
