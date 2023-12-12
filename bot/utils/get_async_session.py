import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, async_scoped_session

from bot.config_reader import DB_URI


def get_async_session():
    engine = create_async_engine(DB_URI)
    session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)
    return session_factory
