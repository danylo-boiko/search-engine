from collections import defaultdict

from bson import ObjectId

from common.enums import Language
from index.repositories import PageRepository, ContentItemRepository
from index.schemas import PageMatch, ContentMatch
from index.services import EmbeddingService


class SearchService:
    def __init__(self) -> None:
        self._page_repository = PageRepository()
        self._content_item_repository = ContentItemRepository()
        self._embedding_service = EmbeddingService()

    def find_pages(self, query: str, language: Language) -> list[PageMatch]:
        page_content_matches = self._get_page_content_matches(query, language)

        pages = self._page_repository.get_by_ids(set(page_content_matches.keys()))

        return [PageMatch(page.title, page.url, page_content_matches[page.id]) for page in pages]

    def _get_page_content_matches(self, query: str, language: Language) -> dict[ObjectId, list[ContentMatch]]:
        query_embedding = self._embedding_service.encode(query)

        page_content_matches = defaultdict(list)

        for content_item in self._content_item_repository.get_similar(query_embedding, language):
            page_content_matches[content_item["page"]].append(
                ContentMatch(content_item["content"], content_item["score"])
            )

        return page_content_matches
