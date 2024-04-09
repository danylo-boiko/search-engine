from mongoengine import Document, StringField, ReferenceField, EnumField, CASCADE

from common.enums import Language
from index.models.page import Page


class ContentItem(Document):
    page = ReferenceField(Page, required=True, reverse_delete_rule=CASCADE)
    content = StringField(required=True)
    language = EnumField(Language, required=True)
