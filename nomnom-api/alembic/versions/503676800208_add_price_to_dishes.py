"""add price to dishes

Revision ID: 503676800208
Revises: 2439a16239bf
Create Date: 2026-06-24 17:31:55.331467

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '503676800208'
down_revision: Union[str, Sequence[str], None] = '2439a16239bf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("dishes", sa.Column("price", sa.Numeric(10, 2), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("dishes", "price")
