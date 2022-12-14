from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from database.pgcommands.commands import ItemCommand, UserCommand, WishlistCommand
from keyboards.callback_factories import ItemCallback
from keyboards.inline import GetInlineKeyboardMarkup
from src import strings

router = Router()


@router.callback_query(ItemCallback.filter(F.action == 'gift'))
async def gift_item_handler(call: types.CallbackQuery, state: FSMContext, callback_data: ItemCallback):
    await state.clear()
    count_gifts = await UserCommand.count_user_gifts(call.from_user.id, callback_data.wishlist_id)
    if count_gifts >= 3:
        await call.answer(strings.item_limit, show_alert=True)
        return
    item_id = callback_data.item_id
    wishlist = await WishlistCommand.get(callback_data.wishlist_id)
    # if wishlist.creator_tg_id == call.from_user.id:
    #     is_owner = True
    # else:
    #     is_owner = False
    is_not_gifted = await ItemCommand.gift(call.from_user.id, item_id)
    # item = await ItemCommand.get(item_id)
    # markup = GetInlineKeyboardMarkup.item_markup(
    #     item=item,
    #     wishlist_hashcode=wishlist.hashcode,
    #     is_owner=is_owner
    # )
    # await call.message.edit_reply_markup(markup)
    if is_not_gifted:
        await WishlistCommand.add_to_related_wishlish(
            user_tg_id=call.from_user.id,
            wishlist_id=wishlist.id,
        )
        await call.answer(strings.item_gifted, show_alert=True)
    else:
        await call.answer(strings.seems_that_someone_gift_it, show_alert=True)
