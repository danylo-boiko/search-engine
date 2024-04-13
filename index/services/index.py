from logging import info

from lingua import LanguageDetectorBuilder

from common import settings
from common.enums import Language
from index.builders import PageBuilder, ContentItemBuilder
from index.repositories import PageRepository, ContentItemRepository
from index.services import EmbeddingService


class IndexService:
    def __init__(self) -> None:
        self._page_repository = PageRepository()
        self._content_item_repository = ContentItemRepository()
        self._embedding_service = EmbeddingService()
        self._language_detector = LanguageDetectorBuilder.from_all_languages().with_preloaded_language_models().build()

    def index_page(self, title: str, url: str, content_items: list[str]) -> None:
        supported_content_items, languages = self._get_supported_content_item_languages(content_items)

        if not supported_content_items:
            return

        created_page = self._page_repository.create(
            PageBuilder()
            .with_title(title)
            .with_url(url)
            .with_content_items(supported_content_items)
        )

        if not created_page:
            return

        embeddings = self._embedding_service.encode_range(supported_content_items)

        content_item_builders = list()

        for content, language, embedding in zip(supported_content_items, languages, embeddings):
            content_item_builders.append(
                ContentItemBuilder()
                .with_page(created_page)
                .with_content(content)
                .with_language(language)
                .with_embedding(embedding)
            )

        self._content_item_repository.create_range(content_item_builders)

        info(f"Indexed page '{created_page.title}' object id '{created_page.id}'")

    def _get_supported_content_item_languages(self, content_items: list[str]) -> tuple[list[str], list[Language]]:
        languages = self._language_detector.detect_languages_in_parallel_of(content_items)

        supported_content_items, supported_languages = list(), list()

        for content_item, language in zip(content_items, languages):
            if language not in settings.supported_languages_lingua:
                continue

            supported_content_items.append(content_item)
            supported_languages.append(Language.from_lingua_language(language))

        return supported_content_items, supported_languages
