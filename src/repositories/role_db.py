from models.role import Role
from repositories.postgres_db import PostgresDB


class RoleDB(PostgresDB):
    table = Role
