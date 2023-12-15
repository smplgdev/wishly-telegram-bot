import sqlalchemy as sa
from sqlalchemy import Column, DateTime, BigInteger, String, Date, Boolean, ForeignKey

from bot.db.base import Base


class TimeBasedModel(Base):
    __abstract__ = True

    created_at = Column(DateTime(timezone=True), default=sa.func.now())
    updated_at = Column(DateTime(timezone=True), default=sa.func.now(), onupdate=sa.func.now())


class AnyList(TimeBasedModel):
    __abstract__ = True

    id = Column(BigInteger, primary_key=True)
    creator_id = Column(BigInteger, ForeignKey('users.id'))

    hashcode = Column(String(6), unique=True)
    title = Column(String(64))
    expiration_date = Column(Date)

    is_active = Column(Boolean, default=True)

    def __repr__(self) -> str:
        return (f'<{self.__class__.__name__}('
                f'id={self.id}, '
                f'creator_id={self.creator_id}, '
                f'title="{self.title}", '
                f'expiration_date={self.expiration_date}'
                ')>')
