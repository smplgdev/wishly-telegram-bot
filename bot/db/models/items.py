from sqlalchemy import ForeignKey, BigInteger, Column, String, Integer

from bot.db.models.abstract import TimeBasedModel


class Item(TimeBasedModel):
    __tablename__ = 'items'

    id = Column(BigInteger, primary_key=True)
    wishlist_id = Column(Integer, ForeignKey('wishlists.id', ondelete="CASCADE"))
    customer_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))

    title = Column(String(64))
    description = Column(String(512))
    photo_link = Column(String(100))
    price = Column(String(50))
    photo_file_id = Column(String(200))
    thumb_link = Column(String(100))

    def __repr__(self) -> str:
        return (f'<Item('
                f'id={self.id}, '
                f'wishlist_id={self.wishlist_id}, '
                f'customer_id={self.customer_id}, '
                f'title="{self.title}"'
                f')>')
