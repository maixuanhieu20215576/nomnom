"""create dishes table

Revision ID: 2439a16239bf
Revises: bc1a916d66d7
Create Date: 2026-06-24 17:14:49.567500

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geography
from pgvector.sqlalchemy import Vector


# revision identifiers, used by Alembic.
revision: str = '2439a16239bf'
down_revision: Union[str, Sequence[str], None] = 'bc1a916d66d7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")

    op.create_table(
        "dishes",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("location", Geography(geometry_type="POINT", srid=4326), nullable=False),
        sa.Column("address_text", sa.Text(), nullable=True),
        sa.Column("food_vector", Vector(384), nullable=True),
        sa.Column("avg_rating", sa.Numeric(3, 2), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
            nullable=False,
        ),
    )

    op.execute("CREATE INDEX idx_dishes_food_vector ON dishes USING ivfflat (food_vector vector_cosine_ops)")


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("idx_dishes_food_vector", table_name="dishes")
    op.drop_table("dishes")
