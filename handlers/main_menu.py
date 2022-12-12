from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from database.pgcommands.commands import UserCommand
from keyboards.callback_factories import WishlistCallback
from keyboards.default import GetKeyboardMarkup
from src import strings

router = Router()


@router.callback_query(WishlistCallback.filter(F.action == 'main_menu'))
async def main_menu_handler(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.delete_reply_markup()
    user = await UserCommand.get(call.from_user.id)
    await call.message.answer(strings.start_text(user_first_name=call.from_user.first_name),
                              reply_markup=GetKeyboardMarkup.start(user.name))
