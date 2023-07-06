import os
from logging import config as logging_config

from pydantic import BaseSettings

from core.logger import LOGGING


class ProjectSettings(BaseSettings):
    # Название проекта. Используется в Swagger-документации
    PROJECT_NAME: str = "Auth"

    # Корень проекта
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    BACKOFF_MAX_TIME: int = 60

    class Config:
        env_file = ".env"


class RedisSettings(BaseSettings):
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    CACHE_EXPIRE_IN_SECONDS: int = 3600

    class Config:
        env_file = ".env"


class PostgresSettings(BaseSettings):
    # Настройки Postgres
    POSTGRES_HOST: str = "postgres"
    POSTGRES_PORT: int = 5432
    POSTGRES_DATABASE: str = "database"
    POSTGRES_USER: str = "user"
    POSTGRES_PASSWORD: str = "pass"

    class Config:
        env_file = ".env"


class AuthjwtSettings(BaseSettings):
    authjwt_secret_key: str = "secret_key"
    authjwt_access_token_expires: int = 900
    authjwt_token_location: set = {"cookies"}
    authjwt_cookie_secure: bool = False
    authjwt_cookie_csrf_protect: bool = False

    class Config:
        env_file = ".env"


project_settings = ProjectSettings()
redis_setttings = RedisSettings()
postgres_settings = PostgresSettings()
auth_settings = AuthjwtSettings()

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)
