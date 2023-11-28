from sqlalchemy import ForeignKey, BigInteger, Column, String, Integer

from bot.db.models.abstract import TimeBasedModel


class Item(TimeBasedModel):
    __tablename__ = 'items'

    id = Column(BigInteger, primary_key=True)
    wishlist_id = Column(Integer, ForeignKey('wishlists.id'))
    customer_id = Column(Integer, ForeignKey('users.id'))

    title = Column(String(64))
    description = Column(String(512))
    photo_link = Column(String(100))
    price = Column(String(50))
    photo_file_id = Column(String(200))
    thumb_link = Column(String(100))
