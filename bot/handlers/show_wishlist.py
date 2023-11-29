from aiogram import Router, F, types, Bot
from sqlalchemy.ext.asyncio import AsyncSession

from bot import strings
from bot.db.models import Wishlist
from bot.db.queries.users import get_user_or_none_by_id, get_user_or_none_by_telegram_id
from bot.db.queries.wishlists import get_wishlist_by_id
from bot.keyboards.callback_factories import WishlistActionsCallback
from bot.keyboards.inline import wishlist_items_keyboard

router = Router()


@router.callback_query(WishlistActionsCallback.filter(F.action == "show_wishlist"))
async def show_wishlist_handler(call: types.CallbackQuery,
                                session: AsyncSession,
                                bot: Bot,
                                callback_data: WishlistActionsCallback):
    await call.answer(cache_time=5)
    wishlist_id = callback_data.wishlist_id
    wishlist = await get_wishlist_by_id(session, wishlist_id)
    await show_wishlist(
        session=session,
        bot=bot,
        user_telegram_id=call.from_user.id,
        wishlist=wishlist,
    )


async def show_wishlist(
        session: AsyncSession,
        bot: Bot,
        user_telegram_id: int,
        wishlist: Wishlist,
):
    """
    Shows selected wishlist description and button that shows gifts. If owner: also edit wishlist button
    """
    owner = await get_user_or_none_by_id(session, wishlist.creator_id)
    if owner.telegram_id == user_telegram_id:
        is_owner = True
    else:
        is_owner = False
    
    markup = wishlist_items_keyboard(
        wishlist_id=wishlist.id,
        wishlist_hashcode=wishlist.hashcode,
        is_owner=is_owner
    )

    text = strings.wishlist_detailed_information(wishlist, owner)
    await bot.send_message(user_telegram_id, text, reply_markup=markup)


# Where is this function used????
#
# @router.callback_query(ItemCallback.filter(F.action == 'show'))
# async def show_item(call: types.CallbackQuery, callback_data: ItemCallback):
#     item_id = callback_data.item_id
#     item = await ItemCommand.get(item_id)
#     text = strings.item_info_text(title=item.title, description=item.description)
#     wishlist = await WishlistCommand.get(item.wishlist_id)
#     if wishlist.creator_tg_id == call.from_user.id:
#         is_owner = True
#     else:
#         is_owner = False
#
#     markup = GetInlineKeyboardMarkup.item_markup(
#         item=item,
#         wishlist_hashcode=wishlist.wishlist_hashcode,
#         is_owner=is_owner
#     )
#
#     if item.photo_file_id is None:
#         await call.message.edit_text(text, reply_markup=markup)
#     else:
#         await call.message.answer_photo(item.photo_file_id, caption=text, reply_markup=markup)
#     await call.answer(cache_time=5)
