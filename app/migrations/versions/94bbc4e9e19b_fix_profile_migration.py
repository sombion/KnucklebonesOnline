"""Fix profile migration

Revision ID: 94bbc4e9e19b
Revises: 1eeb8f101bb9
Create Date: 2024-08-25 23:54:36.448256

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '94bbc4e9e19b'
down_revision: Union[str, None] = '1eeb8f101bb9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('trophies', sa.Integer(), nullable=False))
    op.add_column('user', sa.Column('money', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'money')
    op.drop_column('user', 'trophies')
    # ### end Alembic commands ###
