from re import compile, sub

from bs4 import BeautifulSoup

from crawler.content_extractors import BaseExtractor
from crawler.utils import extract_domain
from localization.enums import Language


class WikipediaExtractor(BaseExtractor):
    def __init__(self, scheme: str, domain: str) -> None:
        super().__init__(scheme, domain)

    @staticmethod
    def get_allowed_subdomains() -> set[str]:
        return {".wikipedia.org"}

    def get_page_language(self) -> Language:
        return Language(self.domain.split(".")[0])

    def extract_title(self, page: BeautifulSoup) -> str:
        return page.title.text

    def extract_content(self, page: BeautifulSoup) -> str:
        cite_pattern = compile(r"\[\w+]")

        content_items = [page.find(id="firstHeading")]
        content_items.extend(page.find(id="mw-content-text").find_all("p"))

        filtered_texts = []

        for item in content_items:
            item_text = sub(cite_pattern, "", item.get_text().replace("\n", ""))

            if not item_text or item_text.isspace():
                continue

            if not item_text.endswith("."):
                item_text += "."

            filtered_texts.append(item_text)

        return " ".join(filtered_texts)

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
