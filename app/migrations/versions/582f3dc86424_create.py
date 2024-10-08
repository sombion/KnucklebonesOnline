"""Create

Revision ID: 582f3dc86424
Revises: 5162354d6676
Create Date: 2024-09-06 20:59:53.078032

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '582f3dc86424'
down_revision: Union[str, None] = '5162354d6676'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('shop_info',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('url', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('inventory',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('id_item', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_item'], ['shop_info.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('user', sa.Column('id_inventory', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('activate_url', sa.String(), nullable=True))
    op.create_foreign_key(None, 'user', 'inventory', ['id_inventory'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_column('user', 'activate_url')
    op.drop_column('user', 'id_inventory')
    op.drop_table('inventory')
    op.drop_table('shop_info')
    # ### end Alembic commands ###
