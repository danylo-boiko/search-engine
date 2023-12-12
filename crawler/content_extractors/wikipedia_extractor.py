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
        content_items = [page.find(id="firstHeading")]

        for tag in page.find(id="mw-content-text").find_all(["p", "ul", "ol", "table"]):
            if tag.name == "p":
                content_items.append(tag)
            elif tag.name in ("ul", "ol") and not (tag.has_attr("class") and "references" in tag["class"]):
                content_items.extend(tag.find_all("li"))
            elif tag.name == "table":
                for row in tag.find_all("tr"):
                    content_items.extend(row.find_all("td"))

        return " ".join(filter(None, [item.get_text(strip=True, separator=" ") for item in content_items]))

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
