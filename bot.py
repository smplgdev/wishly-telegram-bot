import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from redis import Redis

from database.db_gino import db
from handlers import start, gift_ideas, create_wishlist, add_item, main_menu, show_wishlist, gift_item, settings, \
    edit_wishlist, find_wishlist, delete_item_from_wishlist, echo_handler, hide_wishlist
from config import config
from handlers.admin import update_keyboard
from handlers.errors import error_handler
from handlers.inline import show_wishlist_inline, non_logged_users_inline
from src.utils.set_bot_commands import set_bot_commands
from src.utils.set_scheduled_jobs import set_scheduled_jobs

logging.basicConfig(level=logging.INFO)
POSTGRES_URI = f'postgresql://{config.PG_USERNAME}:{config.PG_PASSWORD}@{config.ip}/{config.PG_DATABASE}'

bot = Bot(
    token=config.BOT_TOKEN.get_secret_value(),
    parse_mode='HTML'
)


async def main():
    scheduler = AsyncIOScheduler()
    set_scheduled_jobs(scheduler, bot)

    logging.info("Setup connection with PostgreSQL")
    await db.set_bind(POSTGRES_URI)

    logging.info("Create models")
    await db.gino.create_all()

    redis = Redis(
        host=config.redis_ip,
        port=6379
    )
    storage = RedisStorage(redis=redis)

    dp = Dispatcher(storage=storage)

    dp.include_router(error_handler.error_router)

    dp.include_router(update_keyboard.admin_router)

    dp.include_router(non_logged_users_inline.router)
    dp.include_router(show_wishlist_inline.router)

    dp.include_router(hide_wishlist.router)
    dp.include_router(main_menu.router)
    dp.include_router(start.router)
    dp.include_router(gift_ideas.router)
    dp.include_router(show_wishlist.router)
    dp.include_router(gift_item.router)
    dp.include_router(find_wishlist.router)
    dp.include_router(delete_item_from_wishlist.router)
    dp.include_router(edit_wishlist.router)
    dp.include_router(settings.router)
    dp.include_router(create_wishlist.router)
    dp.include_router(add_item.router)

    dp.include_router(echo_handler.echo_router)

    await set_bot_commands(bot)

    # Launch bot & skip all missed messages
    # await bot.delete_webhook(drop_pending_updates=True)

    logging.info("Starting bot...")
    try:
        scheduler.start()
        await dp.start_polling(bot, storage=storage)
    finally:
        await dp.storage.close()
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())
