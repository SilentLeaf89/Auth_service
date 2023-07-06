from models.user_history import UserHistory
from repositories.postgres_db import PostgresDB


class UserHistoryDB(PostgresDB):
    table = UserHistory
