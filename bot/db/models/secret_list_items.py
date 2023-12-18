from sqlalchemy import Column, Integer, ForeignKey, BigInteger, String
from sqlalchemy.orm import relationship

from bot.db.models.abstract import TimeBasedModel


class SecretListItem(TimeBasedModel):
    __tablename__ = 'secret_list_items'

    id = Column(Integer, primary_key=True)
    participant_id = Column(BigInteger, ForeignKey('secret_list_participants.id', ondelete="CASCADE"))

    title = Column(String(64))
    description = Column(String(512))
    photo_link = Column(String(100))
    price = Column(String(50))
    photo_file_id = Column(String(200))
    thumb_link = Column(String(100))

    participant = relationship('SecretListParticipant', back_populates="items")
