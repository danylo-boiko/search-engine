from modules.index.models import Page, ContentItem


class ContentItemRepository:
    def create_content_items(self, page: Page, content_items: list[str]) -> None:
        ContentItem.objects.insert([
            ContentItem(page=page, content=content_item) for content_item in content_items
        ], load_bulk=False)
