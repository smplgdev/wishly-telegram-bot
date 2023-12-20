from time import strftime

from sqlalchemy import Date, Column, String, ForeignKey, BigInteger, Boolean
from sqlalchemy.orm import relationship

from bot.db.models.wishlist_user_association import wishlist_user_association
from bot.db.models.abstract import TimeBasedModel


class Wishlist(TimeBasedModel):
    __tablename__ = 'wishlists'

    id = Column(BigInteger, primary_key=True)
    creator_id = Column(BigInteger, ForeignKey('users.id', ondelete="CASCADE"))

    hashcode = Column(String(6), unique=True)
    title = Column(String(64))
    purpose = Column(String(length=30))
    expiration_date = Column(Date)

    is_active = Column(Boolean, default=True)

    items = relationship("Item", lazy='selectin')
    users = relationship("User", secondary=wishlist_user_association, back_populates="wishlists", lazy="selectin")

    def __repr__(self) -> str:
        return (f'<{self.__class__.__name__}('
                f'id={self.id}, '
                f'creator_id={self.creator_id}, '
                f'title="{self.title}", '
                f'purpose="{self.purpose}", '
                f'expiration_date={self.expiration_date}'
                ')>')
