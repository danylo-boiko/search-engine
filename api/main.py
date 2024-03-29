from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.settings import settings
from api.v1 import api_router


app = FastAPI(title=settings.PROJECT_TITLE)

app.add_middleware(CORSMiddleware, allow_methods=["GET"])

app.include_router(api_router, prefix=settings.V1_PREFIX)
