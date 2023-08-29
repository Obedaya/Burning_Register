
import secrets
from pydantic import EmailStr, MongoDsn
from pydantic_settings import BaseSettings
from burningbackend import __version__
from burningbackend.app.core.enums import LogLevel

class Settings(BaseSettings):
    # Application
    PROJECT_NAME: str = "Burning Register API"
    PROJECT_VERSION: str = __version__
    API_V1_STR: str = "v1"
    DEBUG: bool = True
    # CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000"]'
    CORS_ORIGINS: list[str] = []
    USE_CORRELATION_ID: bool = True

    UVICORN_HOST: str
    UVICORN_PORT: int

    # Logging
    LOG_LEVEL: str = LogLevel.INFO

    # MongoDB
    MONGODB_URI: str = "mongodb://db:27017/"  # type: ignore[assignment]
    MONGODB_DB_NAME: str = "burningregister"

    # Superuser
    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_EMAIL: EmailStr
    FIRST_SUPERUSER_PASSWORD: str

    # Authentication
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 1  # 60 minutes * 24 hours * 1 = 1 day
    SECRET_KEY: str = secrets.token_urlsafe(32)
    class Config:
        # Place your .env file under this path
        env_file = ".env"
        env_prefix = "BURNINGBACKEND_"
        case_sensitive = True

settings = Settings()  # type: ignore[call-arg]