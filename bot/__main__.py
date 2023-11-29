import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from bot.config_reader import config, DB_URI
from bot.handlers import add_item, main_menu, show_wishlist, edit_wishlist, gift_item, delete_item_from_wishlist
from bot.handlers.inline import show_wishlist_inline, non_logged_users_inline, show_gift_ideas
from bot.middlewares.db import DbSessionMiddleware
from bot.utils.scheduled_jobs import set_scheduled_jobs
from bot.utils.ui_commands import set_ui_commands

logging.basicConfig(level=logging.INFO)

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
    dp.include_router(main_menu.main_menu_router)
    dp.include_router(main_menu.router)
    dp.include_router(add_item.router)
    dp.include_router(show_wishlist.router)
    dp.include_router(edit_wishlist.router)
    dp.include_router(gift_item.router)
    dp.include_router(delete_item_from_wishlist.router)

    # Inline handlers
    dp.include_router(show_gift_ideas.router)
    dp.include_router(show_wishlist_inline.router)
    dp.include_router(non_logged_users_inline.router)
    # dp.include_router(error_handler.error_router)

    # Set bot commands in UI
    await set_ui_commands(bot)

    try:
        # scheduler.start()
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await dp.storage.close()
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())
