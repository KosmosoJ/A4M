"""added slug to models

Revision ID: 31e01284ee91
Revises: 4f7fa2e321c1
Create Date: 2024-10-16 01:55:22.329866

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '31e01284ee91'
down_revision: Union[str, None] = '4f7fa2e321c1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('anime', sa.Column('slug', sa.String(), nullable=True))
    op.add_column('categories', sa.Column('slug', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('categories', 'slug')
    op.drop_column('anime', 'slug')
    # ### end Alembic commands ###