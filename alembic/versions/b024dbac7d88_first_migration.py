"""first migration

Revision ID: b024dbac7d88
Revises:
Create Date: 2023-06-23 03:36:34.267869

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b024dbac7d88"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column("id", sa.UUID, unique=True, primary_key=True),
        sa.Column("created_at", sa.DateTime),
        sa.Column("login", sa.String(255), unique=True, nullable=False),
        sa.Column("password", sa.String(255), nullable=False),
        sa.Column("first_name", sa.String(50)),
        sa.Column("last_name", sa.String(50)),
        sa.Column("history", sa.String(1000), nullable=True),
        sa.Column(
            "role_id", sa.UUID(as_uuid=True), unique=True, nullable=True
        ),
    )

    op.create_table(
        "role",
        sa.Column("id", sa.UUID, unique=True, primary_key=True),
        sa.Column("created_at", sa.DateTime),
        sa.Column("name", sa.String(255), unique=True, nullable=False),
        sa.Column("access", sa.String(255), nullable=True),
    )

    op.create_table(
        "refresh_token",
        sa.Column("id", sa.UUID, unique=True, primary_key=True),
        sa.Column("created_at", sa.DateTime),
        sa.Column("token", sa.String(1000)),
        sa.Column("user_id", sa.UUID),
    )

    op.create_table(
        "user_history",
        sa.Column("id", sa.UUID, unique=True, primary_key=True),
        sa.Column("created_at", sa.DateTime),
        sa.Column("event", sa.String(255)),
        sa.Column("user_id", sa.UUID),
    )

def downgrade() -> None:
    op.drop_table("user")
    op.drop_table("role")
    op.drop_table("refresh_token")
    op.drop_table("user_history")
