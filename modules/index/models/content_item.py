from mongoengine import Document, StringField, ReferenceField

from modules.index.models import Page


class ContentItem(Document):
    page = ReferenceField(Page)
    content = StringField(required=True)
