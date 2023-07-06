import logging
from sqlalchemy.ext.asyncio import create_async_engine

from core.config import postgres_settings
from core.logger import LOGGING

from .db import construct_db_url

db_url = construct_db_url(
    user=postgres_settings.POSTGRES_USER,
    password=postgres_settings.POSTGRES_PASSWORD,
    host=postgres_settings.POSTGRES_HOST,
    port=postgres_settings.POSTGRES_PORT,
    database=postgres_settings.POSTGRES_DATABASE,
)

pg_engine = create_async_engine(db_url, echo=True, future=True)

logging.config.dictConfig(LOGGING)
logger = logging.getLogger()
