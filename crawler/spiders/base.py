from urllib.parse import urlparse, unquote

from scrapy import Spider
from scrapy.crawler import Crawler
from scrapy.http import Response

from common.utils import remove_punctuation
from crawler.settings import MIN_WORDS_IN_CONTENT_ITEM


class BaseSpider(Spider):
    def __init__(self, name: str, **kwargs: dict[str, str]) -> None:
        super().__init__(name)

        start_url, queue = kwargs.get("start_url"), kwargs.get("queue")

        if not start_url and not queue:
            raise RuntimeError("You must specify either 'start_url' or 'queue'")

        if isinstance(start_url, str):
            self.start_urls = [start_url]
            self.queue = self._get_domain(start_url)
        else:
            self.queue = queue

        self.allowed_domains = [self.queue]

    def _get_domain(self, url: str) -> str:
        return urlparse(url).netloc

    def _get_path(self, url: str) -> str:
        return unquote(urlparse(url).path)

    def _get_title(self, response: Response) -> str:
        return response.css("title::text").get().strip()

    def _get_urls(self, response: Response, ignore_other_domains: bool = True) -> set[str]:
        urls = set()

        ancestor_domain = self._get_domain(response.url)

        for sub_url in response.css("a::attr(href)").getall():
            url = response.urljoin(sub_url)

            if not ignore_other_domains or self._get_domain(url) == ancestor_domain:
                urls.add(url)

        return urls

    def _set_crawler(self, crawler: Crawler) -> None:
        super()._set_crawler(crawler)
        self.crawler.settings.set("JOBDIR", f"crawler/jobs/{self.name}/{self.queue}")

    def _has_required_words_count(self, content_item: str) -> bool:
        words = [word for word in remove_punctuation(content_item).split() if word.isalpha()]
        return len(words) >= MIN_WORDS_IN_CONTENT_ITEM
