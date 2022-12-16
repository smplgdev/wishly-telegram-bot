from aiogram import Router, F, types
from aiogram.types import ReplyKeyboardRemove

from database.pgcommands.commands import WishlistCommand
from keyboards.callback_factories import WishlistCallback
from src import strings

router = Router()


@router.callback_query(WishlistCallback.filter(F.action == 'hide'))
async def hide_wishlist_handler(call: types.CallbackQuery, callback_data: WishlistCallback):
    wishlist_id = callback_data.wishlist_id
    await WishlistCommand.remove_from_related(
        user_tg_id=call.from_user.id,
        wishlist_id=wishlist_id
    )
    await call.message.delete_reply_markup()
    await call.message.edit_text(
        text=strings.wishlist_was_hide,
    )
