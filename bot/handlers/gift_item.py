from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from database.pgcommands.commands import ItemCommand, UserCommand, WishlistCommand
from filters.is_logged_user import IsLoggedUserFilter
from keyboards.callback_factories import ItemCallback

import strings

router = Router()


@router.callback_query(IsLoggedUserFilter(is_logged=False))
async def non_logged_users_handler(call: types.CallbackQuery):
    await call.answer(strings.not_logged_user, show_alert=True)


@router.callback_query(ItemCallback.filter(F.action == 'gift'))
async def gift_item_handler(call: types.CallbackQuery, state: FSMContext, callback_data: ItemCallback):
    await state.clear()
    count_gifts = await UserCommand.count_user_gifts(call.from_user.id, callback_data.wishlist_id)
    if count_gifts >= 3:
        await call.answer(
            text=strings.item_limit,
            show_alert=True
        )
        return
    item_id = callback_data.item_id
    wishlist = await WishlistCommand.get(callback_data.wishlist_id)
    if wishlist.creator_tg_id == call.from_user.id:
        await call.answer(
            text=strings.you_cant_gift_yourself,
            show_alert=True
        )
        return

    is_success = await ItemCommand.gift(call.from_user.id, item_id)
    if not is_success:
        await call.answer(
            text=strings.seems_that_someone_gift_it,
            show_alert=True
        )
        return

    await WishlistCommand.add_to_related_wishlish(
        user_tg_id=call.from_user.id,
        wishlist_id=wishlist.id,
    )
    await call.answer(
        strings.item_gifted,
        show_alert=True
    )
