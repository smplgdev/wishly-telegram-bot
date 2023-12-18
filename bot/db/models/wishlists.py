from sqlalchemy import Date, Column, String, ForeignKey, BigInteger, Boolean, Integer
from sqlalchemy.orm import relationship

from bot.db.models.wishlist_user_association import wishlist_user_association
from bot.db.models.abstract import AnyList


class Wishlist(AnyList):
    __tablename__ = 'wishlists'

    items = relationship("Item", lazy='selectin')
    users = relationship("User", secondary=wishlist_user_association, back_populates="wishlists", lazy="selectin")

    participant_id = Column(Integer, ForeignKey('secret_list_participants.id', ondelete="CASCADE"), unique=True)
