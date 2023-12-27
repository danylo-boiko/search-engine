from re import compile, sub

from bs4 import BeautifulSoup

from crawler.content_extractors import BaseExtractor
from crawler.utils import extract_domain
from localization.enums import Language


class WikipediaExtractor(BaseExtractor):
    def __init__(self, scheme: str, domain: str) -> None:
        super().__init__(scheme, domain)
        self.cite_pattern = compile(r"\[\w+]")

    @staticmethod
    def get_allowed_subdomains() -> set[str]:
        return {".wikipedia.org"}

    def get_page_language(self) -> Language:
        return Language(self.domain.split(".")[0])

    def extract_title(self, page: BeautifulSoup) -> str:
        return page.title.text

    def extract_content_items(self, page: BeautifulSoup) -> list[str]:
        content_items = []

        for item in page.find(id="mw-content-text").find_all("p"):
            item_text = sub(self.cite_pattern, "", item.get_text().replace("\n", ""))

            if not item_text or item_text.isspace():
                continue

            if not item_text.endswith("."):
                item_text += "."

            content_items.append(item_text)

        return content_items

    def extract_urls(self, page: BeautifulSoup) -> set[str]:
        urls = set()

        for hyperlink in page.find(id="bodyContent").find_all("a", href=compile(r"/wiki/")):
            url = hyperlink["href"]

            if url.startswith("/wiki/"):
                url = f"{self.scheme}://{self.domain}{url}"

            if extract_domain(url) != self.domain:
                continue

            urls.add(url)

        return urls
