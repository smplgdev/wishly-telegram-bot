from aiogram import Bot
from aiogram.types import BotCommand

bot_commands = {
    "home": "Главное меню",
    "new_wishlist": "Создать новый вишлист",
    "my_wishlists": "Получить список моих вишлистов",
    "find": "Найти вишлист друга по хэшу",
    "name": "Изменить отображаемое имя"
}


async def set_bot_commands(bot: Bot):
    await bot.set_my_commands(commands=[
        BotCommand(command=k, description=v) for k, v in bot_commands.items()
    ])
