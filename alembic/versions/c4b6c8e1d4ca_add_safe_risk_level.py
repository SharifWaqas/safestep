"""add safe risk level

Revision ID: c4b6c8e1d4ca
Revises:
Create Date: 2026-08-12 17:09:49.472365

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c4b6c8e1d4ca'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TYPE risk_level ADD VALUE 'SAFE' BEFORE 'LOW';")

def downgrade() -> None:
    """Downgrade schema."""
    pass
