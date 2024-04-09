from fastapi import FastAPI
from mongoengine import connect, disconnect
from starlette.middleware.cors import CORSMiddleware

from api.settings import settings
from api.v1 import api_router
from common import settings as common_settings


app = FastAPI(
    title=settings.project_title,
    on_startup=[lambda: connect(common_settings.db_name, host=common_settings.db_connection_string)],
    on_shutdown=[disconnect]
)

app.add_middleware(CORSMiddleware, allow_methods=["GET"])

app.include_router(api_router, prefix=settings.v1_prefix)
