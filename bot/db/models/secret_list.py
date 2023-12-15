from sqlalchemy import Column, Integer

from bot.db.models.abstract import TimeBasedModel, AnyList


class SecretList(AnyList):
    __tablename__ = 'secret_lists'

    users_limit = Column(Integer)
    gifts_limit = Column(Integer)
