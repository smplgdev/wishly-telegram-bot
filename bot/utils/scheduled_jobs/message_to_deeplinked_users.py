from aiogram.exceptions import TelegramNotFound

from bot import strings
from bot.__main__ import bot
from bot.db.queries.users import get_user_or_none_by_telegram_id, update_user, get_user_or_none_by_id
from bot.db.queries.wishlists import get_wishlist_by_id
from bot.keyboards.inline import add_items_keyboard, wishlist_items_keyboard
from bot.utils.get_async_session import get_async_session


async def send_message_to_deeplinked_user(
        user_telegram_id: int,
        wishlist_id: int
):
    session = get_async_session()
    async with session.begin() as session:
        user = await get_user_or_none_by_telegram_id(session, telegram_id=user_telegram_id)
        wishlist = await get_wishlist_by_id(session, wishlist_id)
        if not wishlist.is_active:
            return
        user_items = list(filter(lambda item: item.wishlist_id == wishlist.id, user.items))
        wishlist_unselected_items = list(filter(lambda item: not item.customer_id, wishlist.items))
        owner = await get_user_or_none_by_id(session, wishlist.creator_id)
        if len(user_items) == 0 and len(wishlist.items) > 0:
            if len(wishlist_unselected_items) == 0:
                try:
                    await bot.send_message(
                        chat_id=owner.telegram_id,
                        text=strings.your_wishlist_is_full(wishlist.title),
                        reply_markup=add_items_keyboard(wishlist_id)
                    )
                except TelegramNotFound:
                    await update_user(session, user, is_active=False)
            else:
                try:
                    await bot.send_message(
                        chat_id=user_telegram_id,
                        text=strings.you_havent_selected_any_item_in_wishlist(wishlist.title),
                        reply_markup=wishlist_items_keyboard(
                            wishlist_id=wishlist_id,
                            wishlist_hashcode=wishlist.hashcode,
                            is_owner=False,
                            is_admin=False,
                        )
                    )
                except TelegramNotFound:
                    await update_user(session, user, is_active=False)
