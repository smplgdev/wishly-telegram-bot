from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from bot import strings
from bot.keyboards.callback_factories import MainMenuCallback
from bot.keyboards.default import start_keyboard


main_menu_router = Router()


@main_menu_router.callback_query(MainMenuCallback.filter())
async def main_menu_handler(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.delete_reply_markup()
    await call.message.answer(
        strings.start_text(call.from_user.first_name),
        reply_markup=start_keyboard()
    )
