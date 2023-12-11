from urllib.parse import urlparse


def extract_scheme(url: str) -> str:
    return urlparse(url).scheme


def extract_domain(url: str) -> str:
    return urlparse(url).netloc
