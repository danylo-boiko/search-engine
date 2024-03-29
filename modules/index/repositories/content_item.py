from modules.index.models import Page, ContentItem


class ContentItemRepository:
    def create_content_item(self, page: Page, content: str) -> ContentItem:
        return ContentItem(page=page, content=content).save()
