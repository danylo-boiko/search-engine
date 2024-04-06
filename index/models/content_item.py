from mongoengine import Document, StringField, ReferenceField

from index.models.page import Page


class ContentItem(Document):
    page = ReferenceField(Page, db_field="page_id")
    content = StringField(required=True)
