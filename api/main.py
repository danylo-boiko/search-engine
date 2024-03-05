from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.settings import settings
from api.v1.api import api_router


app = FastAPI(title=settings.API_PROJECT_TITLE)

if settings.CORS_ORIGINS:
    app.add_middleware(CORSMiddleware, allow_origins=settings.CORS_ORIGINS, allow_methods=["GET"])

app.include_router(api_router, prefix=settings.API_V1_PREFIX)
