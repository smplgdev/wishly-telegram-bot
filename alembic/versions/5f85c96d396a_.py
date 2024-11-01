"""empty message

Revision ID: 5f85c96d396a
Revises: 7e7bd76edba5
Create Date: 2023-12-17 18:42:25.105941

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5f85c96d396a'
down_revision: Union[str, None] = '7e7bd76edba5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('secret_list_participants', sa.Column('wishlist_id', sa.BigInteger(), nullable=True))
    op.create_foreign_key(None, 'secret_list_participants', 'wishlists', ['wishlist_id'], ['id'], ondelete='CASCADE')
    op.drop_column('secret_list_participants', 'is_gift_selected')
    op.add_column('wishlists', sa.Column('participant_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'wishlists', 'secret_list_participants', ['participant_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'wishlists', type_='foreignkey')
    op.drop_column('wishlists', 'participant_id')
    op.add_column('secret_list_participants', sa.Column('is_gift_selected', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'secret_list_participants', type_='foreignkey')
    op.drop_column('secret_list_participants', 'wishlist_id')
    # ### end Alembic commands ###
