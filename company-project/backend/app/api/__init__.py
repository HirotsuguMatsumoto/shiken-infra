from app.api import companys, items, users, utils
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(utils.router, tags=["utils"])
api_router.include_router(users.router, tags=["users"])
api_router.include_router(items.router, tags=["items"])
api_router.include_router(companys.router, tags=["companys"])
