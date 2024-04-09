from re import sub
from typing import Iterable
from urllib.parse import urlparse

from scrapy import Request
from scrapy.http import Response

from common.enums import Language
from crawler.items import CrawledPage
from crawler.spiders.base import BaseSpider


class WikipediaSpider(BaseSpider):
    name = "wikipedia"

    def __init__(self, **kwargs: dict[str, str]) -> None:
        super().__init__(self.name, **kwargs)

        self.language = Language(self.queue[:2])

        self.sub_paths_to_ignore_content = {
            Language.ENGLISH: ["wikipedia", "category", "help", "list", "file"],
            Language.UKRAINIAN: ["вікіпедія", "категорія", "довідка", "список", "файл"]
        }

    def parse(self, response: Response, **kwargs: dict) -> Iterable[CrawledPage | Request]:
        for url in self._get_urls(response):
            yield Request(url, self.parse)

        if self.__content_has_to_be_ignored(response.url):
            return

        yield CrawledPage(
            title=self._get_title(response),
            url=response.url,
            content_items=self.__parse_content_items(response)
        )

    def __content_has_to_be_ignored(self, url: str) -> bool:
        path = urlparse(url).path.lower()

        for sub_path in self.sub_paths_to_ignore_content[self.language]:
            if path.startswith(f"/wiki/{sub_path}:"):
                return True

        return False

    def __parse_content_items(self, response: Response) -> list[str]:
        content_items = []

        for paragraph in response.css("div#mw-content-text p:not(:has(table)):not(:has(ul)):not(:has(ol))"):
            paragraph_content = "".join(item for item in paragraph.css("::text").extract())

            paragraph_content = self.__clean_paragraph_content(paragraph_content)

            if not paragraph_content.endswith("."):
                paragraph_content += "."

            if self.__is_list_header(paragraph_content) or not self._has_required_words_count(paragraph_content):
                continue

            content_items.append(paragraph_content)

        return content_items

    def __clean_paragraph_content(self, content: str) -> str:
        # remove cites
        content = sub(r"\[[^]]*]", "", content)

        # remove breaks
        content = content.replace("\n", "")

        # remove consecutive dots
        content = sub(r"\.{2,}", "", content)

        # remove consecutive spaces
        content = sub(r"\s{2,}", " ", content)

        return content.strip()

    def __is_list_header(self, text: str) -> bool:
        return text.endswith(":")
