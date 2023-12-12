from hashlib import md5
from logging import info, warning
from threading import get_ident, Thread
from urllib.robotparser import RobotFileParser

from bs4 import BeautifulSoup
from requests import get, RequestException

from crawler.content_extractors import ExtractorsFactory
from crawler.core import SerializableQueue
from crawler.utils import extract_domain, extract_scheme


class Crawler:
    def __init__(self, url: str | None, queue_prefix: str | None, threads_count: int) -> None:
        self.queue = SerializableQueue(url, queue_prefix)
        self.content_extractor = ExtractorsFactory.build(self.queue.head())
        self.threads = [Thread(target=self.__crawl) for _ in range(threads_count)]
        self.is_running = False
        self.robots = {}

    def start(self) -> None:
        self.is_running = True

        for thread in self.threads:
            thread.start()

    def stop(self) -> None:
        self.is_running = False

        for thread in self.threads:
            thread.join()

        self.queue.save_to_file()

    def __crawl(self) -> None:
        while self.is_running:
            url = self.queue.get(timeout=1)

            if not url:
                info(f"Thread {get_ident()} has no new urls for crawling")
                continue

            page = self.__fetch_page(url)

            if not page:
                continue

            content = self.content_extractor.extract_content(page)
            content_hash = self.__compute_content_hash(content)

            print(url, content, content_hash)

            for url in self.content_extractor.extract_urls(page):
                if self.__is_fetch_allowed(url):
                    self.queue.put(url)

    def __fetch_page(self, url: str) -> BeautifulSoup | None:
        try:
            response = get(url, timeout=(3, 30))

            if response.status_code != 200:
                return None

            return BeautifulSoup(response.content, "html.parser")
        except RequestException:
            warning(f"Downloading content from url {url} failed")

    def __is_fetch_allowed(self, url: str) -> bool:
        domain = extract_domain(url)

        if domain not in self.robots:
            scheme = extract_scheme(url)

            parser = RobotFileParser(f"{scheme}://{domain}/robots.txt")
            parser.read()

            self.robots[domain] = parser

        return self.robots[domain].can_fetch("*", url)

    def __compute_content_hash(self, content: str) -> str:
        return md5(content.encode()).hexdigest()
