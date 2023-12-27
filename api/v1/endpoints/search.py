from time import time
from uuid import uuid4

from fastapi import APIRouter

from api.core import settings
from api.schemas import SearchResult, ContentResource
from index import IndexPreloader
from localization import LanguageDetector
from localization.enums import Language

router = APIRouter()
language_detector = LanguageDetector()
index_preloader = IndexPreloader()


@router.get("/", response_model=SearchResult)
def search(query: str, preferred_language: Language | None = None) -> SearchResult:
    start_time = time()

    language = language_detector.detect(query)

    if not language:
        language = preferred_language if preferred_language else settings.DEFAULT_LANGUAGE

    pages = list(index_preloader.get_index(language).find_pages(query))

    end_time = time()

    return SearchResult(
        id=str(uuid4()),
        query=query,
        summary=" ".join([" ".join(page["content_items"]) for page in pages]),
        resources=[ContentResource(title=page["title"], url=page["url"]) for page in pages],
        language=language,
        createdAt=end_time,
        timeTaken=end_time - start_time
    )
