import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, async_scoped_session, AsyncSession

from bot.config_reader import DB_URI


def get_async_session():
    engine = create_async_engine(DB_URI)
    async_session = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession, future=True)
    return async_session
