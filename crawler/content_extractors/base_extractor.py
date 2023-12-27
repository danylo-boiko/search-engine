from abc import abstractmethod

from bs4 import BeautifulSoup

from localization.enums import Language


class BaseExtractor:
    def __init__(self, scheme: str, domain: str) -> None:
        self.scheme = scheme
        self.domain = domain

    @staticmethod
    @abstractmethod
    def get_allowed_subdomains() -> set[str]:
        pass

    @abstractmethod
    def get_page_language(self) -> Language:
        pass

    @abstractmethod
    def extract_title(self, page: BeautifulSoup) -> str:
        pass

    @abstractmethod
    def extract_content_items(self, page: BeautifulSoup) -> list[str]:
        pass

    @abstractmethod
    def extract_urls(self, page: BeautifulSoup) -> set[str]:
        pass
