from sqlalchemy import Date, Column, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

from bot.db.models.wishlist_user_association import wishlist_user_association
from bot.db.models.abstract import AnyList


class Wishlist(AnyList):
    __tablename__ = 'wishlists'

    items = relationship("Item", lazy='selectin')
    users = relationship("User", secondary=wishlist_user_association, back_populates="wishlists", lazy="selectin")

    def __repr__(self) -> str:
        return ('<Wishlist('
                f'id={self.id}, '
                f'creator_id={self.creator_id}, '
                f'title="{self.title}", '
                f'expiration_date={self.expiration_date}'
                ')>')
