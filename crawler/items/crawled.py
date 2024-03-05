from dataclasses import dataclass
from hashlib import md5


@dataclass
class CrawledItem:
    title: str
    url: str
    content_items: list[str]

    def compute_content_hash(self) -> str:
        content = "".join(self.content_items).encode()
        return md5(content).hexdigest()
