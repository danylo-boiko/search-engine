from fastapi import APIRouter

from api.v1.routers import search, spell_check


api_router = APIRouter()

api_router.include_router(search.router, prefix="/search")

api_router.include_router(spell_check.router, prefix="/spell-check")
