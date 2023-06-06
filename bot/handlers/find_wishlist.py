from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from database.pgcommands.commands import WishlistCommand
from handlers.show_wishlist import show_wishlist
from keyboards.callback_factories import WishlistCallback
from keyboards.inline import GetInlineKeyboardMarkup
import strings
from states.find_wishlist_states import FindWishlist

router = Router()


@router.message(Command('find'))
@router.message(F.text == strings.find_friends_wishlist)
async def find_friends_wishlist_handler(message: types.Message, state: FSMContext):
    await state.clear()
    related_wishlists = await WishlistCommand.get_related_wishlists(user_tg_id=message.from_user.id)
    markup = GetInlineKeyboardMarkup.list_related_wishlists(related_wishlists)
    await message.answer(
        text=strings.friends_wishlists_below,
        reply_markup=markup
    )


@router.callback_query(WishlistCallback.filter(F.action == 'find_wishlist'))
async def find_wishlist_handler(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer(
        strings.enter_hashcode,
    )
    await state.set_state(FindWishlist.hashcode)


@router.message(FindWishlist.hashcode)
async def change_name_handler(message: types.Message, state: FSMContext):
    hashcode = message.text.replace("#", '')
    wishlist = await WishlistCommand.find_by_hashcode(hashcode)
    if not wishlist:
        await message.answer(strings.cant_find_wishlist)
        return
    await message.answer(strings.found_wishlist)
    await state.clear()
    await show_wishlist(message, message.from_user.id, wishlist)
