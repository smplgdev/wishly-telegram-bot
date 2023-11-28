from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from bot import strings

main_menu_router = Router()


@main_menu_router.message(F.text == strings.gift_ideas)
async def gift_ideas_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.reply("Этот раздел пока что находится в разработке :(")
