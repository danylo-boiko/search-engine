from re import sub
from typing import Iterable

from scrapy import Request
from scrapy.http import Response
from unicodedata import normalize

from common.enums import Language
from crawler.items import CrawledPage
from crawler.spiders.base import BaseSpider


class WikipediaSpider(BaseSpider):
    name = "wikipedia"

    def __init__(self, **kwargs: dict[str, str]) -> None:
        super().__init__(self.name, **kwargs)

        self.language = Language(self.queue.split(".")[0])

        self.sub_paths_to_ignore_content = {
            Language.ENGLISH: ["wikipedia", "category", "help", "list", "file", "template", "portal"],
            Language.UKRAINIAN: ["вікіпедія", "категорія", "довідка", "список", "файл", "шаблон", "портал"]
        }

    def parse(self, response: Response, **kwargs: dict) -> Iterable[CrawledPage | Request]:
        for url in self._get_urls(response):
            yield Request(url, self.parse)

        if self._content_has_to_be_ignored(response.url):
            return

        yield CrawledPage(self._get_title(response), response.url, self._parse_content_items(response))

    def _content_has_to_be_ignored(self, url: str) -> bool:
        path = self._get_path(url).lower()

        for sub_path in self.sub_paths_to_ignore_content[self.language]:
            if path.startswith(f"/wiki/{sub_path}:"):
                return True

        return False

    def _parse_content_items(self, response: Response) -> list[str]:
        content_items = list()

        for paragraph in response.css("div#mw-content-text p:not(:has(table)):not(:has(ul)):not(:has(ol))"):
            paragraph_content = "".join(item for item in paragraph.css("::text").extract())

            paragraph_content = self._clean_content(paragraph_content)

            if not self._has_required_words_count(paragraph_content) or self._is_list_header(paragraph_content):
                continue

            if not paragraph_content.endswith("."):
                paragraph_content += "."

            content_items.append(paragraph_content)

        return content_items

    def _clean_content(self, content: str) -> str:
        # remove \x... characters
        content = normalize("NFKD", content)

        # remove cites
        content = sub(r"\[[^]]*]", "", content)

        # remove breaks
        content = content.replace("\n", " ")

        # remove consecutive dots
        content = sub(r"\.{2,}", "", content)

        # remove consecutive spaces
        content = sub(r"\s{2,}", " ", content)

        return content.strip()

    def _is_list_header(self, content: str) -> bool:
        return content.endswith(":")
