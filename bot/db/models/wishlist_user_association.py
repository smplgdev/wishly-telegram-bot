from sqlalchemy import Column, Table, Integer, ForeignKey

from bot.db.base import Base

wishlist_user_association = Table(
    'wishlist_user_association',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('wishlist_id', Integer, ForeignKey('wishlists.id'))
)
