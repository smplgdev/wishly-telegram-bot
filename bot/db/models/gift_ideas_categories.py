from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from bot.db.models.abstract import TimeBasedModel


class GiftIdeaCategory(TimeBasedModel):
    __tablename__ = 'gift_idea_categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(32), unique=True)
    gift_ideas = relationship("GiftIdea", lazy='selectin')
