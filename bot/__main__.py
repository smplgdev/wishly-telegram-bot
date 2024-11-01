import asyncio
import logging

from aiogram import Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from bot.bot_instance import bot
from bot.config_reader import config, DB_URI
from bot.handlers import add_item, main_menu, show_wishlist, edit_wishlist, gift_item, delete_item_from_wishlist, \
    my_gifts
from bot.handlers.admin import add_wishlist_to_gift_idea, file_id
from bot.handlers.errors import error_handler
from bot.handlers.inline import show_wishlist_inline, non_logged_users_inline, show_gift_ideas
from bot.middlewares.db import DbSessionMiddleware
from bot.middlewares.get_scheduler import SchedulerMiddleware
from bot.utils.scheduled_jobs.set_scheduled_jobs import set_scheduled_jobs_once
from bot.utils.ui_commands import set_ui_commands


def setup_logging():
    """
    Set up logging configuration for the application.

    This method initializes the logging configuration for the application.
    It sets the log level to INFO and configures a basic colorized log for
    output. The log format includes the filename, line number, log level,
    timestamp, logger name, and log message.

    Returns:
        None

    Example usage:
        setup_logging()
    """

    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )
    logger = logging.getLogger(__name__)
    logger.info("Starting bot")


async def main():
    setup_logging()

    engine = create_async_engine(url=DB_URI)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    jobstores = {
        'default': RedisJobStore(jobs_key='dispatched_trips_jobs', run_times_key='dispatched_trips_running',
                                 host=config.REDIS_HOST, port=config.REDIS_PORT)
    }
    scheduler = AsyncIOScheduler(jobstores=jobstores, timezone='Europe/Berlin')

    redis = Redis(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
    )
    storage = RedisStorage(redis=redis)

    # Setup dispatcher and bind routers to it
    dp = Dispatcher(storage=storage)
    dp.update.middleware.register(DbSessionMiddleware(session_pool=sessionmaker))
    dp.update.middleware.register(SchedulerMiddleware(scheduler=scheduler))

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
    dp.include_router(my_gifts.router)

    # Admin handlers
    dp.include_router(add_wishlist_to_gift_idea.admin_router)
    dp.include_router(file_id.admin_router)

    # Error handler
    dp.include_router(error_handler.router)

    # Inline handlers
    dp.include_router(non_logged_users_inline.router)
    dp.include_router(show_gift_ideas.router)
    dp.include_router(show_wishlist_inline.router)

    # Set bot commands in UI
    await set_ui_commands(bot)

    try:
        scheduler.start()
        set_scheduled_jobs_once(scheduler)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await dp.storage.close()
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())
