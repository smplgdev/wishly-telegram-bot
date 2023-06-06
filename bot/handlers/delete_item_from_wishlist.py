from aiogram import Router, F, types

from database.pgcommands.commands import ItemCommand, WishlistCommand
from handlers.show_wishlist import show_wishlist
from keyboards.callback_factories import ItemCallback
import strings

router = Router()


@router.callback_query(ItemCallback.filter(F.action == 'delete'))
async def delete_item_handler(call: types.CallbackQuery, callback_data: ItemCallback):
    item_id = callback_data.item_id
    item = await ItemCommand.delete(item_id)
    wishlist = await WishlistCommand.get(item.wishlist_id)
    await call.answer(strings.item_successfully_deleted, show_alert=True)
    await call.message.delete()
    await show_wishlist(call.message, call.from_user.id, wishlist)
