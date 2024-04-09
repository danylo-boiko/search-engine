from pymongo.command_cursor import CommandCursor

from common.enums import Language
from index.builders import ContentItemBuilder
from index.models import ContentItem


class ContentItemRepository:
    def get_similar(
        self,
        embedding: list[float],
        language: Language,
        top_k: int = 5,
        min_matching_score: float = 0.75
    ) -> CommandCursor:
        return ContentItem.objects.aggregate([{
            "$vectorSearch": {
                "index": "embedding",
                "path": "embedding",
                "queryVector": embedding,
                "numCandidates": top_k * 2000,
                "limit": top_k
            }}, {
            "$project": {
                "page": 1,
                "content": 1,
                "language": 1,
                "matching_score": {"$meta": "vectorSearchScore"}
            }}, {
            "$match": {
                "$and": [
                    {"matching_score": {"$gte": min_matching_score}},
                    {"language": language}
                ]
            }}
        ])

    def create_range(self, content_item_builders: list[ContentItemBuilder]) -> None:
        ContentItem.objects.insert([
            content_item_builder.build() for content_item_builder in content_item_builders
        ], load_bulk=False)
