import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aioredis import Redis
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from handlers.errors import error_handler
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config_reader import config
from middlewares.db import DbSessionMiddleware
from utils.scheduled_jobs import set_scheduled_jobs
from utils.ui_commands import set_ui_commands

logging.basicConfig(level=logging.INFO)
DB_URI = f'postgresql://{config.PG_USERNAME}:{config.PG_PASSWORD}@{config.ip}/{config.PG_DATABASE}'

bot = Bot(
    token=config.BOT_TOKEN.get_secret_value(),
    parse_mode='HTML'
)


async def main():
    engine = create_async_engine(url=DB_URI)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    scheduler = AsyncIOScheduler()
    set_scheduled_jobs(scheduler, bot)

    redis = Redis(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
    )
    storage = RedisStorage(redis=redis)

    # Setup dispatcher and bind routers to it
    dp = Dispatcher(storage=storage)
    dp.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))
    # Automatically reply to all callbacks
    dp.callback_query.middleware(CallbackAnswerMiddleware())

    # Register handlers
    dp.include_router(error_handler.error_router)

    # Set bot commands in UI
    await set_ui_commands(bot)

    try:
        scheduler.start()
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await dp.storage.close()
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())
