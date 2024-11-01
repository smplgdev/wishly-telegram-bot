from aiogram import Bot

from bot.config_reader import config

bot = Bot(
    token=config.BOT_TOKEN.get_secret_value(),
    disable_web_page_preview=True,
    parse_mode='HTML'
)
