from aiogram import Router, F, types

from database.pgcommands.commands import WishlistCommand
from keyboards.callback_factories import WishlistCallback
from keyboards.inline import GetInlineKeyboardMarkup
from src import strings

router = Router()


@router.callback_query(WishlistCallback.filter(F.action == 'edit'))
async def edit_wishlist_handler(call: types.CallbackQuery, callback_data: WishlistCallback):
    wishlist_id = callback_data.wishlist_id
    markup = GetInlineKeyboardMarkup.edit_or_delete_wishlist(wishlist_id)
    await call.message.edit_text(
        text=strings.what_you_want_to_do_with_wishlist,
        reply_markup=markup
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
