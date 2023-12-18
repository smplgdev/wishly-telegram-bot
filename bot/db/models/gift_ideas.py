from sqlalchemy import Column, Integer, String, ForeignKey

from bot.db.models.abstract import TimeBasedModel


class GiftIdea(TimeBasedModel):
    __tablename__ = "gift_ideas"

    id = Column(Integer, primary_key=True)
    gift_idea_category_id = Column(Integer, ForeignKey('gift_idea_categories.id', ondelete="CASCADE"))
    title = Column(String(64))
    description = Column(String(512))
    photo_link = Column(String(100))
    price = Column(String(50))
    photo_file_id = Column(String(200))
    thumb_link = Column(String(100))
