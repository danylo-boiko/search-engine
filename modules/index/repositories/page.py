from mongoengine import NotUniqueError

from modules.common.enums import Language
from modules.index.models import Page


class PageRepository:
    def create_page(self, title: str, url: str, language: Language, content_hash: str) -> Page | None:
        try:
            return Page(title=title, url=url, language=language, content_hash=content_hash).save()
        except NotUniqueError:
            return None
