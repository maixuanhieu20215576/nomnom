"""add role to users

Revision ID: 9b2ed84d17a5
Revises: a8a55b0f2e86
Create Date: 2026-06-25 16:40:01.650200

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM


# revision identifiers, used by Alembic.
revision: str = '9b2ed84d17a5'
down_revision: Union[str, Sequence[str], None] = 'a8a55b0f2e86'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

user_role_enum = ENUM("admin", "user", name="user_role")


def upgrade() -> None:
    """Upgrade schema."""
    user_role_enum.create(op.get_bind())
    op.add_column("users", sa.Column("role", user_role_enum, nullable=False, server_default="user"))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "role")
    user_role_enum.drop(op.get_bind())
