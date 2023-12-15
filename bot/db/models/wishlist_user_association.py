from sqlalchemy import Column, ForeignKey, BigInteger, Table

from bot.db.base import Base


wishlist_user_association = Table(
    'wishlist_user_association',
    Base.metadata,
    Column('user_id', BigInteger, ForeignKey('users.id', ondelete="CASCADE")),
    Column('wishlist_id', BigInteger, ForeignKey('wishlists.id', ondelete="CASCADE"))
)
