import asyncio

from aiogram import Router, Bot
from asyncpg import ForeignKeyViolationError

from database.pgcommands.commands import UserCommand
from handlers.main_menu_message import main_menu_send_message

error_router = Router()


@error_router.errors()
async def error_handler(exception, bot: Bot):
    update = exception.update
    error = exception.exception

    user = await UserCommand.get(update.message.from_user.id)

    try:
        await bot.send_message(
            chat_id=5543936487,
            text="\n".join([
                "Found Error!",
                f"user {user.name}, ID: {user.id} (@{user.username})" if user else "user not found",
                str(error),
                str(update),
            ])
        )
    except:
        pass

    if isinstance(error, ForeignKeyViolationError):
        user = await UserCommand.add(
            tg_id=update.message.from_user.id,
            name=update.message.from_user.first_name,
            deep_link=None,
            username=update.message.from_user.username,
        )

    await update.message.answer("Упс! Произошла ошибка :( Сейчас Вас перенаправит в главное меню.")
    await asyncio.sleep(3)
    await main_menu_send_message(
        bot=bot,
        user_tg_id=update.message.from_user.id,
        user_name=user.name
    )
