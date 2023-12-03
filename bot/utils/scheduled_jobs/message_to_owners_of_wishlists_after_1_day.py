from aiogram.exceptions import TelegramNotFound

from bot import strings
from bot.__main__ import bot
from bot.db.queries.users import get_user_or_none_by_id, update_user
from bot.db.queries.wishlists import get_wishlist_by_id, get_wishlist_related_users
from bot.keyboards.inline import wishlist_items_keyboard
from bot.utils.get_async_session import get_async_session
from bot.utils.send_message import send_message


async def send_message_to_owner_of_wishlist(
        wishlist_id: int
):
    async with get_async_session().begin() as session:

        wishlist = await get_wishlist_by_id(session, wishlist_id)
        if not wishlist.is_active:
            return
        owner = await get_user_or_none_by_id(session, wishlist.creator_id)
        if len(wishlist.items) == 0:
            text = strings.your_wishlist_is_still_empty(wishlist_title=wishlist.title)
        else:
            wishlist_related_users = await get_wishlist_related_users(session, wishlist)
            gifted_items = list(filter(lambda item: item.customer_id, wishlist.items))
            non_gifted_items = list(filter(lambda item: not item.customer_id, wishlist.items))
            text = strings.wishlist_owner_party_soon(
                owner=owner,
                wishlist=wishlist,
                related_users=wishlist_related_users,
                gifted_items=gifted_items,
                non_gifted_items=non_gifted_items,
            )

        is_sent = await send_message(
            bot=bot,
            user_id=owner.telegram_id,
            text=text,
            reply_markup=wishlist_items_keyboard(
                wishlist_id=wishlist.id,
                wishlist_hashcode=wishlist.hashcode,
                is_owner=True,
            )
        )
        if not is_sent:
            await update_user(session, user=owner, is_active=False)
