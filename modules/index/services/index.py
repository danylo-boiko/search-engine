from hashlib import md5

from modules.common.enums import Language
from modules.index.repositories import PageRepository, ContentItemRepository


class IndexService:
    def __init__(self) -> None:
        self.page_repository = PageRepository()
        self.content_item_repository = ContentItemRepository()

    def index_crawled_page(self, title: str, url: str, language: Language, content_items: list[str]) -> None:
        content_hash = md5("".join(content_items).encode()).hexdigest()

        created_page = self.page_repository.create_page(title, url, language, content_hash)

        if not created_page:
            return

        for content_item in content_items:
            self.content_item_repository.create_content_item(created_page, content_item)
