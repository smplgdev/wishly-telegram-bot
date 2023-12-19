import sqlalchemy as sa
from sqlalchemy import Column, DateTime, BigInteger, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from bot.db.base import Base


class TimeBasedModel(Base):
    __abstract__ = True

    created_at = Column(DateTime(timezone=True), default=sa.func.now())
    updated_at = Column(DateTime(timezone=True), default=sa.func.now(), onupdate=sa.func.now())
