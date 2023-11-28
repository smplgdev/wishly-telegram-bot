from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from bot import strings
from bot.db.models import Item
from bot.db.queries.items import get_item_by_id
from bot.db.queries.users import get_user_or_none_by_telegram_id, gift_item
from bot.db.queries.wishlists import get_wishlist_by_id, add_wishlist_to_favourite
from bot.filters.is_logged_user_filter import IsLoggedUserFilter
from bot.keyboards.callback_factories import GiftItemCallback

router = Router()


@router.callback_query(IsLoggedUserFilter(is_logged=False))
async def non_logged_users_handler(call: types.CallbackQuery):
    await call.answer(strings.not_logged_user, show_alert=True)


@router.callback_query(GiftItemCallback.filter())
async def gift_item_handler(
        call: types.CallbackQuery,
        state: FSMContext,
        callback_data: GiftItemCallback,
        session: AsyncSession
):
    await state.clear()
    item_id = callback_data.item_id
    item = await get_item_by_id(session, item_id)
    wishlist = await get_wishlist_by_id(session, item.wishlist_id)
    wishlist_items: list[Item] = wishlist.items
    count_user_gifts = len(list(filter(lambda _item: _item.customer_id == call.from_user.id, wishlist_items)))
    if count_user_gifts == 3:
        await call.answer(
            text=strings.item_limit,
            show_alert=True
        )
        return
    user = await get_user_or_none_by_telegram_id(session, telegram_id=call.from_user.id)

    if wishlist.creator_id == user.id:
        await call.answer(
            text=strings.you_cant_gift_yourself,
            show_alert=True
        )
        return
    item_id = callback_data.item_id
    item = await get_item_by_id(session, item_id)
    gifted_item = await gift_item(session, user=user, item=item)
    if not gifted_item:
        await call.answer(
            text=strings.seems_that_someone_gift_it,
            show_alert=True
        )
        return

    await add_wishlist_to_favourite(session, user, wishlist)

    await call.answer(
        strings.item_gifted,
        show_alert=True
    )
