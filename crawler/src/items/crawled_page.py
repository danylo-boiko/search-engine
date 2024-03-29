from scrapy import Item


class CrawledPage(Item):
    title: str
    url: str
    content_items: list[str]
