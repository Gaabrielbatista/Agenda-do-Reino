"""add cor column to eventos_normais and eventos_recorrentes

Revision ID: 4d5e6f7a8b9c
Revises: 3bdd133fbb6c
Create Date: 2026-06-12 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4d5e6f7a8b9c'
down_revision: Union[str, None] = '3bdd133fbb6c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('eventos_normais', sa.Column('cor', sa.String(7), nullable=True))
    op.add_column('eventos_recorrentes', sa.Column('cor', sa.String(7), nullable=True))


def downgrade() -> None:
    op.drop_column('eventos_recorrentes', 'cor')
    op.drop_column('eventos_normais', 'cor')
