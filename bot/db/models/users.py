from sqlalchemy import String, Boolean, BigInteger, Column
from sqlalchemy.orm import relationship

from bot.db.models.abstract import TimeBasedModel
from bot.db.models.wishlist_user_association import wishlist_user_association


class User(TimeBasedModel):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    telegram_id = Column(BigInteger, unique=True)
    deep_link = Column(String(64))

    name = Column(String(64))
    username = Column(String(32))
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    wishlists = relationship("Wishlist", secondary=wishlist_user_association, lazy='selectin')
    items = relationship("Item", lazy='selectin')