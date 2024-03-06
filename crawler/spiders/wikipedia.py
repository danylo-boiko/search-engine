from re import compile
from typing import Iterable
from urllib.parse import urlparse

from scrapy import Spider, Request
from scrapy.crawler import Crawler
from scrapy.http import Response

from common import settings
from indexer.models import CrawledPage
from localization.enums import Language


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
            title=self.__extract_title(response),
            url=response.url,
            content_items=self.__extract_content_items(response)
        )

        for url in self.__extract_urls_to_crawl(response):
            yield Request(url, self.parse)

    def _set_crawler(self, crawler: Crawler) -> None:
        super()._set_crawler(crawler)
        self.crawler.settings.set("JOBDIR", f"crawler/jobs/{self.queue}")

    def __extract_title(self, response: Response) -> str:
        return response.css("title::text").get()

    def __extract_content_items(self, response: Response) -> list[str]:
        content_items = []

        for paragraph in response.css("div#mw-content-text p"):
            paragraph_items = [item for item in paragraph.css("::text").extract() if not compile(r"\[\d+]").match(item)]

            paragraph_content = "".join(paragraph_items).replace("\n", "").strip()

            if not paragraph_content or paragraph_content[-1] == ":":
                continue

            if not paragraph_content.endswith("."):
                paragraph_content += "."

            content_items.append(paragraph_content)

        return content_items

    def __extract_urls_to_crawl(self, response: Response) -> set[str]:
        response_url = urlparse(response.url)

        urls = set()

        for url in response.css("div#mw-content-text a[href*='/wiki/']::attr(href)").getall():
            if url.startswith("/wiki/"):
                url = f"{response_url.scheme}://{response_url.netloc}{url}"

            if urlparse(url).netloc == response_url.netloc:
                urls.add(url)

        return urls
