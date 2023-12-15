from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot import strings
from bot.handlers.create_list import create_list
from bot.utils.types import ListTypes

main_menu_router = Router()


@main_menu_router.message(F.text == strings.secret_list)
async def secret_list_handler(message: Message, state: FSMContext, bot: Bot):
    await message.answer("Данный раздел пока что находится в разработке :(\n\n"
                         "Вы сможете протестировать его через несколько дней")
    return
    await create_list(
        bot=bot,
        user_id=message.from_user.id,
        list_type=ListTypes.SECRET_LIST,
        state=state
    )
