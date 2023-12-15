from sqlalchemy import Column, ForeignKey, BigInteger, Table
from sqlalchemy.orm import relationship

from bot.db.base import Base


wishlist_user_association = Table(
    'wishlist_user_association',
    Base.metadata,
    Column('user_id', BigInteger, ForeignKey('users.id', ondelete="CASCADE")),
    Column('wishlist_id', BigInteger, ForeignKey('wishlists.id', ondelete="CASCADE"))
)


# class WishlistUserAssociation(Base):
#     __tablename__ = 'wishlist_user_association'
#
#     user_id = Column(BigInteger, ForeignKey('users.id', ondelete="CASCADE"), primary_key=True),
#     wishlist_id = Column(BigInteger, ForeignKey('wishlists.id', ondelete="CASCADE"), primary_key=True)
