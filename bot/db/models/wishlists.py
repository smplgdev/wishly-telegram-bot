from sqlalchemy import Date, Column, String, ForeignKey, Boolean, BigInteger, Integer
from sqlalchemy.orm import relationship

from bot.db.models.abstract import TimeBasedModel


class Wishlist(TimeBasedModel):
    __tablename__ = 'wishlists'

    id = Column(BigInteger, primary_key=True)
    creator_id = Column(Integer, ForeignKey('users.id'))

    hashcode = Column(String(6), unique=True)
    title = Column(String(64))
    expiration_date = Column(Date)

    items = relationship("Item", lazy='selectin')

    is_active = Column(Boolean, default=True)
