from fastapi import APIRouter

from burningbackend.app.api.v1.endpoints import movies, inventory
from burningbackend.app.core.config import settings

router = APIRouter(prefix=f"/{settings.API_V1_STR}")
router.include_router(movies.router, prefix="/movies", tags=["Movies"])
router.include_router(inventory.router, prefix="/inventory", tags=["Inventory"])