from models.refresh_token import RefreshToken
from repositories.postgres_db import PostgresDB


class RefreshTokenDB(PostgresDB):
    table = RefreshToken
