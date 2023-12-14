from time import strftime

from sqlalchemy import Date, Column, String, ForeignKey, Boolean, BigInteger, Integer
from sqlalchemy.orm import relationship

from bot.db.models import wishlist_user_association
from bot.db.models.abstract import TimeBasedModel


class Wishlist(TimeBasedModel):
    __tablename__ = 'wishlists'

    id = Column(BigInteger, primary_key=True)
    creator_id = Column(Integer, ForeignKey('users.id'))

    hashcode = Column(String(6), unique=True)
    title = Column(String(64))
    expiration_date = Column(Date)

    related_users = relationship("User", secondary=wishlist_user_association, lazy="selectin")
    items = relationship("Item", lazy='selectin')

    is_active = Column(Boolean, default=True)

    def __repr__(self) -> str:
        return ('<Wishlist('
                f'id={self.id}, '
                f'creator_id={self.creator_id}, '
                f'title="{self.title}", '
                f'expiration_date={strftime("%d.%m.%Y", self.expiration_date)}'
                ')>')
