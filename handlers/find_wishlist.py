from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from database.pgcommands.commands import WishlistCommand
from handlers.show_wishlist import show_wishlist
from src import strings
from states.find_wishlist_states import FindWishlist

router = Router()


@router.message(Command('find'))
@router.message(F.text == strings.find_friends_wishlist)
async def find_friends_wishlist_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await state.set_state(FindWishlist.hashcode)
    await message.answer(strings.enter_hashcode)


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
