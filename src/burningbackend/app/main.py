from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware


from burningbackend.app.core.config import settings
from burningbackend.app import api
from burningbackend.app.db import init_db

@asynccontextmanager
async def lifespan(application: FastAPI):  # noqa
    await init_db.init()
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    openapi_url=f"/api/{settings.API_V1_STR}/openapi.json",
    docs_url=None,
    lifespan=lifespan,
    license_info={
        "name": "GNU General Public License v3.0",
        "url": "https://www.gnu.org/licenses/gpl-3.0.en.html",
    },
)

#app.mount("/static", StaticFiles(directory="burningbackend/app/static"), name="static")

app.include_router(api.router)

if settings.CORS_ORIGINS:
    from fastapi.middleware.cors import CORSMiddleware

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    