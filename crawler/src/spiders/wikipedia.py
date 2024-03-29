from urllib.parse import urlparse

from scrapy import Spider
from scrapy.crawler import Crawler
from scrapy.http import Response

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

    def parse(self, response: Response, **kwargs: dict) -> None:
        pass

    def _set_crawler(self, crawler: Crawler) -> None:
        super()._set_crawler(crawler)
        self.crawler.settings.set("JOBDIR", f"jobs/{self.queue}")
