from sqlalchemy import Table, Column, BigInteger, ForeignKey

from bot.db.base import Base

secret_list_user_association = Table(
    'secret_list_user_association',
    Base.metadata,
    Column('user_id', BigInteger, ForeignKey('users.id', ondelete="CASCADE")),
    Column('secret_list_id', BigInteger, ForeignKey('secret_lists.id', ondelete="CASCADE"))
)
