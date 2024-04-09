from mongoengine import Document, StringField, DateTimeField


class Page(Document):
    title = StringField(required=True)
    url = StringField(required=True)
    content_hash = StringField(required=True, unique=True)
    created_at = DateTimeField(required=True)
