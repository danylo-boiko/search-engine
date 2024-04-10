from logging import info

from lingua import LanguageDetectorBuilder
from sentence_transformers import SentenceTransformer

from common import settings
from common.enums import Language
from index.builders import PageBuilder, ContentItemBuilder
from index.repositories import PageRepository, ContentItemRepository
from index.schemas import PageMatches, ContentMatching


class IndexService:
    def __init__(self, read_only: bool = False) -> None:
        self._read_only = read_only
        self._page_repository = PageRepository()
        self._content_item_repository = ContentItemRepository()
        self._embedding_model = SentenceTransformer(settings.embedding_model_name)

        if self._read_only:
            return

        self._language_detector = LanguageDetectorBuilder.from_all_languages().with_preloaded_language_models().build()

    def find_pages(self, query: str, language: Language) -> list[PageMatches]:
        content_items = list(self._content_item_repository.get_similar(self._get_embedding(query), language))

        pages = self._page_repository.get_by_ids(set(content_item["page"] for content_item in content_items))

        page_aggregations = list()

        for page in pages:
            page_aggregations.append(PageMatches(
                title=page.title,
                url=page.url,
                content_items=[
                    ContentMatching(content=content_item["content"], score=content_item["matching_score"])
                    for content_item in content_items
                    if content_item["page"] == page.id
                ]
            ))

        return page_aggregations

    def index_page(self, title: str, url: str, content_items: list[str]) -> None:
        if self._read_only:
            raise RuntimeError("The service is running in read-only mode")

        detected_languages = self._language_detector.detect_languages_in_parallel_of(content_items)

        if not any(language in settings.supported_languages_lingua for language in detected_languages):
            return

        created_page = self._page_repository.create(
            PageBuilder()
            .with_title(title)
            .with_url(url)
            .with_content_items(content_items)
        )

        if not created_page:
            return

        content_item_builders = list()

        for content, language in zip(content_items, detected_languages):
            if language not in settings.supported_languages_lingua:
                continue

            content_item_builders.append(
                ContentItemBuilder()
                .with_page(created_page)
                .with_content(content)
                .with_language(Language.from_lingua_language(language))
                .with_embedding(self._get_embedding(content))
            )

        self._content_item_repository.create_range(content_item_builders)

        info(f"Indexed page {created_page.id} {created_page.title}")

    def _get_embedding(self, text: str) -> list[float]:
        return self._embedding_model.encode(text).tolist()
