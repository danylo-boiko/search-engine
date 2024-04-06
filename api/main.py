from fastapi import FastAPI
from mongoengine import connect, disconnect
from starlette.middleware.cors import CORSMiddleware

from api.settings import settings
from api.v1 import api_router
from common import settings as common_settings


app = FastAPI(
    title=settings.PROJECT_TITLE,
    on_startup=[lambda: connect(common_settings.DB_NAME, host=common_settings.DB_CONNECTION_STRING)],
    on_shutdown=[disconnect]
)

app.add_middleware(CORSMiddleware, allow_methods=["GET"])

app.include_router(api_router, prefix=settings.V1_PREFIX)
