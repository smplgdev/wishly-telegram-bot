from sqlalchemy import Integer, Column, BigInteger, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from bot.db.models.abstract import TimeBasedModel


class SecretListParticipant(TimeBasedModel):
    __tablename__ = 'secret_list_participants'

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete="CASCADE"))
    secret_list_id = Column(Integer, ForeignKey('secret_lists.id', ondelete="CASCADE"))
    wishlist_id = Column(BigInteger, ForeignKey('wishlists.id', ondelete="CASCADE"))

    giver_participant_id = Column(BigInteger, ForeignKey('secret_list_participants.id', ondelete="CASCADE"))
    # is_gift_selected = Column(Boolean, default=False)

    user = relationship('User', back_populates="participations", foreign_keys=[user_id], lazy='selectin')
    giver_participant = relationship('SecretListParticipant', uselist=False, remote_side=[id], lazy="selectin")
    wishlist = relationship("Wishlist", lazy="selectin", foreign_keys=wishlist_id)
    secret_list = relationship("SecretList", back_populates="participants", lazy="selectin")

    items = relationship('SecretListItem', back_populates="participant", lazy='selectin')
