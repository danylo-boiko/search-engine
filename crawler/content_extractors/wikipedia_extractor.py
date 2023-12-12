from re import compile

from bs4 import BeautifulSoup

from crawler.content_extractors import BaseExtractor
from crawler.utils import extract_domain


class WikipediaExtractor(BaseExtractor):
    def __init__(self, scheme: str, domain: str) -> None:
        super().__init__(scheme, domain)

    @staticmethod
    def get_allowed_subdomains() -> set[str]:
        return {".wikipedia.org"}

    def extract_content(self, page: BeautifulSoup) -> str:
        return page.find(id="firstHeading").text

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
