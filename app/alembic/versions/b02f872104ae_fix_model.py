"""fix model

Revision ID: b02f872104ae
Revises: 1b0ddfebcfaf
Create Date: 2024-11-03 17:59:36.180607

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b02f872104ae'
down_revision: Union[str, None] = '1b0ddfebcfaf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('images', sa.Column('anime', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'images', 'anime', ['anime'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'images', type_='foreignkey')
    op.drop_column('images', 'anime')
    # ### end Alembic commands ###