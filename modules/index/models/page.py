from time import time

from mongoengine import Document, StringField, EnumField, FloatField

from modules.common.enums import Language


class Page(Document):
    title = StringField(required=True)
    url = StringField(required=True)
    language = EnumField(Language, required=True)
    content_hash = StringField(required=True, unique=True)
    created_at = FloatField(default=time)
