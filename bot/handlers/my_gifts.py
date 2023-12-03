from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot import strings
from bot.db.queries.items import update_item, get_item_by_id
from bot.db.queries.users import get_user_or_none_by_telegram_id
from bot.db.queries.wishlists import get_wishlist_by_id
from bot.keyboards.callback_factories import UserGiftsCallback, DeleteGiftCallback
from bot.keyboards.inline import wishlist_items_keyboard, list_user_items

router = Router()


@router.callback_query(UserGiftsCallback.filter(F.action == "show"))
async def show_users_gifts(
        call: CallbackQuery,
        session: AsyncSession,
        callback_data: UserGiftsCallback
):
    await call.answer()
    wishlist_id = callback_data.wishlist_id
    wishlist = await get_wishlist_by_id(session, wishlist_id)
    user = await get_user_or_none_by_telegram_id(session, call.from_user.id)
    users_gifts = list(filter(lambda item: item.customer_id == user.id, wishlist.items))
    if len(users_gifts) == 0:
        text = strings.no_gifts_yet
        markup = wishlist_items_keyboard(
            wishlist_id=wishlist_id,
            wishlist_hashcode=wishlist.hashcode,
            is_owner=False,
            is_admin=False,
            user_has_gifts=False,
        )
    else:
        markup = list_user_items(users_gifts)
        text = strings.your_gifts_list

    await call.message.answer(
        text,
        reply_markup=markup
    )


@router.callback_query(DeleteGiftCallback.filter())
async def delete_item_from_gifts(
        call: CallbackQuery,
        session: AsyncSession,
        callback_data: DeleteGiftCallback
):
    item_id = callback_data.item_id
    item = await get_item_by_id(session, item_id)
    await update_item(session, item, customer_id=None)

    await call.answer(strings.gift_successfully_deleted(item.title), show_alert=True)
