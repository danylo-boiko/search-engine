from abc import abstractmethod

from bs4 import BeautifulSoup


class BaseExtractor:
    def __init__(self, scheme: str, domain: str) -> None:
        self.scheme = scheme
        self.domain = domain

    @staticmethod
    @abstractmethod
    def get_allowed_subdomains() -> set[str]:
        pass

    @abstractmethod
    def extract_content(self, page: BeautifulSoup) -> str:
        pass

    @abstractmethod
    def extract_urls(self, page: BeautifulSoup) -> set[str]:
        pass
