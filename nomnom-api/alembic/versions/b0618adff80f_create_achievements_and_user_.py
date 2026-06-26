"""create achievements and user_achievements tables

Revision ID: b0618adff80f
Revises: 33eb73d9cf84
Create Date: 2026-06-26 11:00:10.936598

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'b0618adff80f'
down_revision: Union[str, Sequence[str], None] = '33eb73d9cf84'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "achievements",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("icon_object_name", sa.String(length=500), nullable=True),
        sa.Column("criteria", postgresql.JSONB(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "user_achievements",
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), primary_key=True),
        sa.Column("achievement_id", sa.Integer(), sa.ForeignKey("achievements.id"), primary_key=True),
        sa.Column("unlocked_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("user_achievements")
    op.drop_table("achievements")
