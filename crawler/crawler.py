from crawler.content_extractors import ExtractorsFactory


class Crawler:
    def __init__(self, url: str, threads_count: int) -> None:
        self.url = url
        self.threads_count = threads_count
        self.content_extractor = ExtractorsFactory.build(url)

    def run(self) -> None:
        pass
