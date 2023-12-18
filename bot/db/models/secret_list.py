from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from bot.db.models.abstract import AnyList


class SecretList(AnyList):
    __tablename__ = 'secret_lists'

    max_participants = Column(Integer)
    max_gifts = Column(Integer, default=3)

    status = Column(String(10), default="waiting")  # waiting | running | finished
    participants = relationship("SecretListParticipant", back_populates="secret_list", lazy="selectin")
