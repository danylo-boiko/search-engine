from bson import ObjectId
from mongoengine import NotUniqueError

from index.builders import PageBuilder
from index.models import Page


class PageRepository:
    def get_by_ids(self, ids: set[ObjectId]) -> list[Page]:
        return Page.objects.filter(id__in=ids)

    def create(self, page_builder: PageBuilder) -> Page | None:
        try:
            return page_builder.build().save()
        except NotUniqueError:
            return None
