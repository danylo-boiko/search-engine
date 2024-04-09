from itertools import groupby

from mongoengine import get_db

from index.builders import ContentItemBuilder


class ContentItemRepository:
    def __init__(self) -> None:
        self._db = get_db()

    def create_range(self, content_item_builders: list[ContentItemBuilder]) -> None:
        content_items = [content_item_builder.build().to_mongo() for content_item_builder in content_item_builders]

        for language, items in groupby(content_items, lambda item: item["language"]):
            self._db[f"{language}_content_item"].insert_many(items)
