from aiogram import Router, F, types, Bot
from aiogram.fsm.context import FSMContext

from database.pgcommands.commands import UserCommand
from handlers.main_menu_message import main_menu_send_message
from keyboards.callback_factories import WishlistCallback

router = Router()


@router.callback_query(WishlistCallback.filter(F.action == 'main_menu'))
async def main_menu_handler(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    await state.clear()
    await call.message.delete_reply_markup()
    user = await UserCommand.get(call.from_user.id)
    await main_menu_send_message(
        bot,
        user_tg_id=call.from_user.id,
        user_name=user.name
    )
