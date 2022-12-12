from datetime import datetime

from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from database.pgcommands.commands import WishlistCommand
from keyboards.inline import GetInlineKeyboardMarkup
from src import strings
from states.wishlist import CreateWishlist

router = Router()


@router.message(Command('new_wishlist'))
@router.message(F.text == strings.create_wishlist)
async def create_wishlist_handler(message: types.message, state: FSMContext):
    await state.clear()
    await message.answer(strings.enter_wishlist_title)
    await state.set_state(CreateWishlist.title)


@router.message(CreateWishlist.title)
async def create_wishlist_step2(message: types.Message, state: FSMContext):
    if len(message.text) > 64:
        await message.reply(strings.wishlist_title_too_long)
        return
    await state.update_data(wishlist_title=message.text)
    await message.answer(strings.enter_expire_date)
    await state.set_state(CreateWishlist.expiration_date)


@router.message(CreateWishlist.expiration_date)
async def create_wishlist_finish(message: types.Message, state: FSMContext):
    try:
        date = datetime.strptime(message.text, "%d.%m.%Y").date()
    except ValueError:
        await message.reply(strings.date_value_error)
        return
    if date < datetime.today().date():
        await message.reply(strings.past_date_error)
        return
    data = await state.get_data()
    title = data.get("wishlist_title")
    wishlist = await WishlistCommand.add(creator_tg_id=message.from_user.id, title=title, expiration_date=date)
    await message.answer(strings.wishlist_successfully_created(wishlist=wishlist),
                         reply_markup=GetInlineKeyboardMarkup.add_items(wishlist_id=wishlist.id))
    await state.clear()
