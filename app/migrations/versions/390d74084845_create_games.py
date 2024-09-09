"""Create games

Revision ID: 390d74084845
Revises: e08030c5a18a
Create Date: 2024-08-26 19:13:21.886664

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '390d74084845'
down_revision: Union[str, None] = 'e08030c5a18a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('game',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('id_pl1', sa.Integer(), nullable=False),
    sa.Column('id_pl2', sa.Integer(), nullable=False),
    sa.Column('pl1_1_1', sa.Integer(), nullable=False),
    sa.Column('pl1_1_2', sa.Integer(), nullable=False),
    sa.Column('pl1_1_3', sa.Integer(), nullable=False),
    sa.Column('pl1_2_1', sa.Integer(), nullable=False),
    sa.Column('pl1_2_2', sa.Integer(), nullable=False),
    sa.Column('pl1_2_3', sa.Integer(), nullable=False),
    sa.Column('pl1_3_1', sa.Integer(), nullable=False),
    sa.Column('pl1_3_2', sa.Integer(), nullable=False),
    sa.Column('pl1_3_3', sa.Integer(), nullable=False),
    sa.Column('pl1_1', sa.Integer(), sa.Computed('pl1_1_1 + pl1_1_2 + pl1_1_3', ), nullable=False),
    sa.Column('pl1_2', sa.Integer(), sa.Computed('pl1_2_1 + pl1_2_2 + pl1_2_3', ), nullable=False),
    sa.Column('pl1_3', sa.Integer(), sa.Computed('pl1_3_1 + pl1_3_2 + pl1_3_3', ), nullable=False),
    sa.Column('pl1_count', sa.Integer(), sa.Computed('pl1_1 + pl1_2 + pl1_3', ), nullable=False),
    sa.Column('pl2_1_1', sa.Integer(), nullable=False),
    sa.Column('pl2_1_2', sa.Integer(), nullable=False),
    sa.Column('pl2_1_3', sa.Integer(), nullable=False),
    sa.Column('pl2_2_1', sa.Integer(), nullable=False),
    sa.Column('pl2_2_2', sa.Integer(), nullable=False),
    sa.Column('pl2_2_3', sa.Integer(), nullable=False),
    sa.Column('pl2_3_1', sa.Integer(), nullable=False),
    sa.Column('pl2_3_2', sa.Integer(), nullable=False),
    sa.Column('pl2_3_3', sa.Integer(), nullable=False),
    sa.Column('pl2_1', sa.Integer(), sa.Computed('pl2_1_1 + pl2_1_2 + pl2_1_3', ), nullable=False),
    sa.Column('pl2_2', sa.Integer(), sa.Computed('pl2_2_1 + pl2_2_2 + pl2_2_3', ), nullable=False),
    sa.Column('pl2_3', sa.Integer(), sa.Computed('pl2_3_1 + pl2_3_2 + pl2_3_3', ), nullable=False),
    sa.Column('pl2_count', sa.Integer(), sa.Computed('pl2_1 + pl2_2 + pl2_3', ), nullable=False),
    sa.Column('status_games', sa.String(), nullable=False),
    sa.Column('id_pl_win', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_pl1'], ['user.id'], ),
    sa.ForeignKeyConstraint(['id_pl2'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('game')
    # ### end Alembic commands ###
