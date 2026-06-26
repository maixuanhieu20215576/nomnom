"""add country and fruit material tag

Revision ID: 33eb73d9cf84
Revises: 183c599d30a0
Create Date: 2026-06-26 10:31:25.235955

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM


# revision identifiers, used by Alembic.
revision: str = '33eb73d9cf84'
down_revision: Union[str, Sequence[str], None] = '183c599d30a0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

country_enum = ENUM(
    "viet", "thai", "korean", "europe", "japan", "china", "other",
    name="country",
)


def upgrade() -> None:
    """Upgrade schema."""
    with op.get_context().autocommit_block():
        op.execute("ALTER TYPE material_tag ADD VALUE IF NOT EXISTS 'fruit'")

    country_enum.create(op.get_bind())
    op.add_column("dishes", sa.Column("country", country_enum, nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("dishes", "country")
    country_enum.drop(op.get_bind())
    # Postgres does not support removing a single enum value; the 'fruit' value
    # added to material_tag intentionally remains on downgrade.
