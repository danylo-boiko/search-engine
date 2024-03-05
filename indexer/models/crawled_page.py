from dataclasses import dataclass
from hashlib import md5


@dataclass
class CrawledPage:
    title: str
    url: str
    content_items: list[str]

    def get_content_items_hash(self) -> str:
        content = "".join(self.content_items).encode()
        return md5(content).hexdigest()
