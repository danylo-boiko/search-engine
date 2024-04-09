from mongoengine import NotUniqueError

from index.builders import PageBuilder
from index.models import Page


class PageRepository:
    def create(self, page_builder: PageBuilder) -> Page | None:
        try:
            return page_builder.build().save()
        except NotUniqueError:
            return None
