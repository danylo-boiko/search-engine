from urllib.parse import urlparse

from scrapy.http import Response


def get_page_title(response: Response) -> str:
    return response.css("title::text").get()


def get_page_urls(response: Response, ignore_other_domains: bool = True) -> set[str]:
    urls = set()

    for url in response.css("a::attr(href)").getall():
        full_url = response.urljoin(url)

        if not ignore_other_domains or urlparse(full_url).netloc == urlparse(response.url).netloc:
            urls.add(full_url)

    return urls
