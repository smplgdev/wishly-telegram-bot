from sqlalchemy import Column, Integer

from bot.db.models.abstract import TimeBasedModel, AnyList


class SecretList(AnyList):
    __tablename__ = 'secret_lists'

    max_participants = Column(Integer)
    max_gifts = Column(Integer)
