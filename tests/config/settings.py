from typing import Optional

from dotenv import find_dotenv, load_dotenv
from pydantic import BaseSettings

load_dotenv()


class TestSettings(BaseSettings):
    # Настройки Redis
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379

    # Настройки основного сервиса
    SERVICE_URL: str = "fastapi"

    # Настройки логирования
    LOGGER_FORMATTER: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOGGER_LEVEL: str = "DEBUG"
    LOGGER_FILE: Optional[str] = "/tests/logs/tests.log"

    class Config:
        env_file = find_dotenv(".env.tests")


class Dsn(BaseSettings):
    dbname: str = "database"
    user: str = "user"
    password: str = "mysecretpassword"
    host: str = "postgres"
    port: int = 5432
    # options: str = '-c search_path=content'

    class Config:
        env_file = find_dotenv(".env.tests")


test_settings = TestSettings()
dsn = Dsn()
