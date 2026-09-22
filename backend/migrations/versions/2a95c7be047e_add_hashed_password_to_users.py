"""Add hashed_password to users

Revision ID: 2a95c7be047e
Revises: 
Create Date: 2026-09-21 15:13:52.084385

"""
from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = '2a95c7be047e'
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""


def downgrade() -> None:
    """Downgrade schema."""
