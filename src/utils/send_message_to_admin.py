from aiogram import Bot

from config import config


async def send_message_to_admin(bot: Bot):
    admins = config.ADMINS
    for admin in admins:
        await bot.send_message(
            chat_id=admin,
            text="Sending messages will start in 5 minutes",
        )
