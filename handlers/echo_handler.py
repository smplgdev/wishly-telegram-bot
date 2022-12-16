from aiogram import Router, types

from database.pgcommands.commands import UserCommand
from keyboards.default import GetKeyboardMarkup
from src import strings

echo_router = Router()


@echo_router.message()
async def echo_handler(message: types.Message):
    if message.via_bot:
        return
    user_tg_id = message.from_user.id
    user = await UserCommand.update(
            user_tg_id=user_tg_id,
            username=message.from_user.username
    )
    await message.answer(
        strings.start_text(message.from_user.first_name),
        reply_markup=GetKeyboardMarkup.start(user_name=user.name)
    )
