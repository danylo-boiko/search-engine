from crawler.content_extractors import BaseExtractor, WikipediaExtractor
from crawler.utils import extract_domain, extract_scheme


class ExtractorsFactory:
    @staticmethod
    def build(url: str) -> BaseExtractor:
        domain = extract_domain(url)

        for allowed_subdomain in WikipediaExtractor.get_allowed_subdomains():
            if domain.endswith(allowed_subdomain):
                return WikipediaExtractor(extract_scheme(url), domain)

        raise NotImplementedError(f"Url {url} is not supported")
