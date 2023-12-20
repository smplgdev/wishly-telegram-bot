import asyncio
import logging

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from bot import strings
from bot.bot_instance import bot
from bot import config_reader as config
from bot.db.queries.users import get_user_or_none_by_id, update_user
from bot.db.queries.wishlists import get_all_parties_wishlists_in_days
from bot.keyboards.inline import wishlist_items_keyboard
from bot.utils.get_async_session import get_async_session
from bot.utils.send_message import send_message


async def party_is_soon_message():
    async_session = get_async_session()
    async with async_session() as session:
        wishlists = await get_all_parties_wishlists_in_days(session, days=[3, 7])
        logging.info("I found wishlists: " + str(len(list(wishlists))))
        for wishlist in wishlists:
            owner = await get_user_or_none_by_id(session, wishlist.creator_id)

            wishlist_related_users = wishlist.users
            logging.info(f"\nWishlist {wishlist}\nUsers: {len(wishlist_related_users)}")

            for user in wishlist_related_users:
                if not user.is_active:
                    logging.info("User skipped due to deactivation – %s" % user)
                    continue
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
    logging.info("Function %s is finished" % party_is_soon_message.__name__)
