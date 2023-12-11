from abc import abstractmethod


class BaseExtractor:
    def __init__(self, scheme: str, domain: str) -> None:
        self.scheme = scheme
        self.domain = domain

    @staticmethod
    @abstractmethod
    def get_allowed_subdomains() -> set[str]:
        pass
