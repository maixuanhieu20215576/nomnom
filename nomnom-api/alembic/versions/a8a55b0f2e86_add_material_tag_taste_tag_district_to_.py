"""add material_tag taste_tag district to dishes

Revision ID: a8a55b0f2e86
Revises: 80fe0020ba83
Create Date: 2026-06-25 10:13:14.496970

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM


# revision identifiers, used by Alembic.
revision: str = 'a8a55b0f2e86'
down_revision: Union[str, Sequence[str], None] = '80fe0020ba83'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

material_tag_enum = ENUM(
    "pork", "beef", "chicken", "duck", "vegetables", "noodle", "seafood", "rice", "fish",
    name="material_tag",
)
taste_tag_enum = ENUM(
    "spicy", "sweet", "bitter", "neutral", "salty", "sour", "savory", "greasy",
    name="taste_tag",
)


def upgrade() -> None:
    """Upgrade schema."""
    material_tag_enum.create(op.get_bind())
    taste_tag_enum.create(op.get_bind())

    op.add_column("dishes", sa.Column("district", sa.Text(), nullable=True))
    op.add_column("dishes", sa.Column("material_tag", sa.ARRAY(material_tag_enum), nullable=True))
    op.add_column("dishes", sa.Column("taste_tag", sa.ARRAY(taste_tag_enum), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("dishes", "taste_tag")
    op.drop_column("dishes", "material_tag")
    op.drop_column("dishes", "district")

    taste_tag_enum.drop(op.get_bind())
    material_tag_enum.drop(op.get_bind())
