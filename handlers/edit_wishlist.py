import asyncio
import datetime

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from database.pgcommands.commands import WishlistCommand
from handlers.show_wishlist import show_wishlist
from keyboards.callback_factories import WishlistCallback
from keyboards.inline import GetInlineKeyboardMarkup
from src import strings
from states.wishlist import CreateWishlist

router = Router()


@router.callback_query(WishlistCallback.filter(F.action == 'edit'))
async def edit_wishlist_handler(call: types.CallbackQuery, callback_data: WishlistCallback):
    await call.answer(cache_time=20)
    wishlist_id = callback_data.wishlist_id
    markup = GetInlineKeyboardMarkup.edit_or_delete_wishlist(wishlist_id)
    await call.message.answer(
        text=strings.what_you_want_to_do_with_wishlist,
        reply_markup=markup
    )


@router.callback_query(WishlistCallback.filter(F.action == 'change_date'))
async def change_date_handler_step1(
        call: types.CallbackQuery,
        state: FSMContext,
        callback_data: WishlistCallback
):
    await call.answer(cache_time=20)
    wishlist_id = callback_data.wishlist_id
    wishlist = await WishlistCommand.get(wishlist_id)
    markup = GetInlineKeyboardMarkup.go_back_to_wishlist(wishlist_id)
    await state.update_data(wishlist_id=wishlist_id)
    await state.set_state(CreateWishlist.change_date)
    await call.message.edit_text(
        text=strings.enter_new_expire_date(current_date=wishlist.expiration_date),
        reply_markup=markup
    )


@router.message(CreateWishlist.change_date, F.content_type == 'text')
async def change_date_handler_step2(message: types.Message, state: FSMContext):
    try:
        date = datetime.datetime.strptime(message.text, "%d.%m.%Y").date()
    except ValueError:
        await message.reply(strings.date_value_error)
        return
    if date < datetime.datetime.today().date():
        await message.reply(strings.past_date_error)
        return
    data = await state.get_data()
    wishlist_id = data.get("wishlist_id")
    await WishlistCommand.update(
        wishlist_id=wishlist_id,
        expiration_date=date
    )
    wishlist = await WishlistCommand.get(wishlist_id)
    await message.answer(strings.date_successfully_changed)
    await asyncio.sleep(1)
    await show_wishlist(
        message=message,
        user_id=message.from_user.id,
        wishlist=wishlist
    )


@router.callback_query(WishlistCallback.filter(F.action == 'change_title'))
async def change_title_handler_step1(
        call: types.CallbackQuery,
        state: FSMContext,
        callback_data: WishlistCallback
):
    await call.answer(cache_time=20)
    wishlist_id = callback_data.wishlist_id
    markup = GetInlineKeyboardMarkup.go_back_to_wishlist(wishlist_id)
    await state.update_data(wishlist_id=wishlist_id)
    await state.set_state(CreateWishlist.change_name)
    await call.message.edit_text(
        text=strings.write_new_title,
        reply_markup=markup
    )


@router.message(CreateWishlist.change_name, F.content_type == 'text')
async def change_title_handler_step2(message: types.Message, state: FSMContext):
    data = await state.get_data()
    new_title = message.text
    if len(new_title) > 64:
        await message.reply(strings.wishlist_title_too_long)
        return
    wishlist_id = data.get("wishlist_id")
    await WishlistCommand.update(
        wishlist_id=wishlist_id,
        title=new_title
    )
    wishlist = await WishlistCommand.get(wishlist_id)
    await message.answer(strings.title_successfully_changed)
    await asyncio.sleep(1)
    await show_wishlist(
        message=message,
        user_id=message.from_user.id,
        wishlist=wishlist
    )


@router.callback_query(WishlistCallback.filter(F.action == 'delete_wishlist'))
async def delete_wishlist_handler(call: types.CallbackQuery, callback_data: WishlistCallback):
    wishlist_id = callback_data.wishlist_id
    markup = GetInlineKeyboardMarkup.delete_wishlist_or_not(wishlist_id)
    await call.message.edit_text(strings.are_you_sure_to_delete_wishlist,
                                 reply_markup=markup)


@router.callback_query(WishlistCallback.filter(F.action == 'no_delete'))
async def no_delete_handler(call: types.CallbackQuery):
    await call.answer(strings.delete_cancel, show_alert=True)
    await call.message.delete()


@router.callback_query(WishlistCallback.filter(F.action == 'yes_delete'))
async def no_delete_handler(call: types.CallbackQuery, callback_data: WishlistCallback):
    wishlist_id = callback_data.wishlist_id
    await WishlistCommand.make_inactive(wishlist_id)
    await call.answer(strings.delete_successful, show_alert=True)
    await call.message.delete()
