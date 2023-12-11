from crawler.content_extractors import BaseExtractor


class WikipediaExtractor(BaseExtractor):
    def __init__(self, scheme: str, domain: str) -> None:
        super().__init__(scheme, domain)

    @staticmethod
    def get_allowed_subdomains() -> set[str]:
        return {".wikipedia.org"}
