from logging import info

from lingua import LanguageDetectorBuilder

from common import settings
from common.enums import Language
from index.builders import PageBuilder, ContentItemBuilder
from index.repositories import PageRepository, ContentItemRepository


class IndexService:
    def __init__(self) -> None:
        self._page_repository = PageRepository()
        self._content_item_repository = ContentItemRepository()
        self._language_detector = LanguageDetectorBuilder.from_all_languages().with_preloaded_language_models().build()

    def index_page(self, title: str, url: str, content_items: list[str]) -> None:
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

        content_item_builders = []

        for content, language in zip(content_items, detected_languages):
            if language not in settings.supported_languages_lingua:
                continue

            content_item_builders.append(
                ContentItemBuilder()
                .with_page(created_page)
                .with_content(content)
                .with_language(Language.from_lingua_language(language))
            )

        self._content_item_repository.create_range(content_item_builders)

        info(f"Indexed page {created_page.id} {created_page.title}")
