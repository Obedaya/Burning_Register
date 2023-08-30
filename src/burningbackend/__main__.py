import uvicorn

from burningbackend.app.core.config import settings


def run_dev_server() -> None:
    """Run the uvicorn server in development environment."""
    uvicorn.run(
        "burningbackend.app.main:app",  # path to the ASGI application
        host=settings.UVICORN_HOST,
        port=settings.UVICORN_PORT,
        reload=settings.DEBUG,
    )


if __name__ == "__main__":
    run_dev_server()