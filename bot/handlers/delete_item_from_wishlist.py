import asyncio

from aiogram import Router, types, Bot
from sqlalchemy.ext.asyncio import AsyncSession

from bot import strings
from bot.db.queries.items import delete_item, get_item_by_id
from bot.db.queries.wishlists import get_wishlist_by_id
from bot.handlers.show_wishlist import show_wishlist
from bot.keyboards.callback_factories import DeleteItemCallback

router = Router()


@router.callback_query(DeleteItemCallback.filter())
async def delete_item_handler(
        call: types.CallbackQuery,
        callback_data: DeleteItemCallback,
        session: AsyncSession,
        bot: Bot,
):
    item_id = callback_data.item_id
    item = await get_item_by_id(session, item_id)
    if not item:
        await call.answer(strings.item_already_deleted)
        return
    if item.customer_id:
        await call.answer(strings.we_cant_delete_item, show_alert=True)
        return
    await delete_item(session, item)
    wishlist = await get_wishlist_by_id(session, item.wishlist_id)
    await call.answer(strings.item_successfully_deleted, show_alert=True)
    await show_wishlist(session, bot, call.from_user.id, wishlist)
