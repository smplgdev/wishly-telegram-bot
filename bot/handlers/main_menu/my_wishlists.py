from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from bot import strings
from bot.db.models import User
from bot.keyboards.inline import list_user_wishlists

main_menu_router = Router()


@main_menu_router.message(F.text == strings.my_wishlists)
async def show_my_wishlists_handler(message: types.Message, state: FSMContext, user: User):
    await state.clear()
    user_wishlists = list(filter(lambda wishlist: wishlist.is_active, user.wishlists))
    markup = list_user_wishlists(user_wishlists, user_id=user.id)
    await message.answer(strings.your_wishlists, reply_markup=markup)
