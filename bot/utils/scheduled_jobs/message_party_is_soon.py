import asyncio
import logging

from bot import strings
from bot.bot_instance import bot
from bot.db.queries.users import get_user_or_none_by_id, update_user
from bot.db.queries.wishlists import get_all_parties_wishlists_in_days
from bot.keyboards.inline import wishlist_items_keyboard
from bot.utils.get_async_session import get_async_session
from bot.utils.send_message import send_message


async def party_is_soon_message():
    async with get_async_session().begin() as session:
        wishlists = list()
        for days_before_celebration in [3, 7]:
            wishlists_to_add = await get_all_parties_wishlists_in_days(session, days=days_before_celebration)
            for wishlist in list(wishlists_to_add):
                wishlists.append(wishlist)
        logging.info("I found wishlists: " + str(len(list(wishlists))))
        for wishlist in wishlists:
            owner = await get_user_or_none_by_id(session, wishlist.creator_id)

            wishlist_related_users = wishlist.users
            logging.info(f"\nWishlist {wishlist}\nUsers: {len(wishlist_related_users)}")

            for user in wishlist_related_users:
                customer_items = list(filter(lambda item_: item_.customer_id == user.id, wishlist.items))
                if len(customer_items) == 0:
                    user_has_gifts = False
                else:
                    user_has_gifts = True
                text = strings.party_soon(
                    wishlist=wishlist,
                    owner=owner,
                    items=customer_items
                )
                markup = wishlist_items_keyboard(
                    wishlist_id=wishlist.id,
                    wishlist_hashcode=wishlist.hashcode,
                    is_owner=False,
                    is_admin=False,
                    user_has_gifts=user_has_gifts
                )
                is_sent = await send_message(
                    bot=bot,
                    user_id=user.telegram_id,
                    text=text,
                    reply_markup=markup
                )
                await asyncio.sleep(0.04)
                if not is_sent:
                    await update_user(session, user=user, is_active=False)


