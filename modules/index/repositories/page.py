from mongoengine import NotUniqueError

from modules.common.enums import Language
from modules.index.models import Page


class PageRepository:
    def create_page(self, title: str, url: str, content_hash: str) -> Page | None:
        try:
            return Page(title=title, url=url, content_hash=content_hash).save()
        except NotUniqueError:
            return None
