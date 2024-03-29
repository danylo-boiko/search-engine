from hashlib import md5

from modules.common.enums import Language
from modules.index.repositories import PageRepository, ContentItemRepository


class IndexService:
    def __init__(self) -> None:
        self._page_repository = PageRepository()
        self._content_item_repository = ContentItemRepository()

    def index_crawled_page(self, title: str, url: str, language: Language, content_items: list[str]) -> None:
        created_page = self._page_repository.create_page(title, url, language, self._get_content_hash(content_items))

        if not created_page:
            return

        self._content_item_repository.create_content_items(created_page, content_items)

    def find_indexed_pages(self, query: str, language: Language) -> list:
        return []

    def _get_content_hash(self, content_items: list[str]) -> str:
        encoded_content = "".join(content_items).encode()
        return md5(encoded_content).hexdigest()
