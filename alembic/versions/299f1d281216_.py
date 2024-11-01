"""empty message

Revision ID: 299f1d281216
Revises: ee2b0a7ff57f
Create Date: 2023-12-15 16:03:28.190097

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '299f1d281216'
down_revision: Union[str, None] = 'ee2b0a7ff57f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('secret_lists', sa.Column('max_participants', sa.Integer(), nullable=True))
    op.add_column('secret_lists', sa.Column('max_gifts', sa.Integer(), nullable=True))
    op.drop_column('secret_lists', 'users_limit')
    op.drop_column('secret_lists', 'gifts_limit')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('secret_lists', sa.Column('gifts_limit', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('secret_lists', sa.Column('users_limit', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('secret_lists', 'max_gifts')
    op.drop_column('secret_lists', 'max_participants')
    # ### end Alembic commands ###
