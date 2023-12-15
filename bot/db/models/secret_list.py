from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from bot.db.models.abstract import TimeBasedModel, AnyList
from bot.db.models.secret_list_user_association import secret_list_user_association


class SecretList(AnyList):
    __tablename__ = 'secret_lists'

    max_participants = Column(Integer)
    max_gifts = Column(Integer)

    users = relationship("User", secondary=secret_list_user_association, back_populates="secret_lists", lazy="selectin")
