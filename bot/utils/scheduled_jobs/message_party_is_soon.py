import asyncio

from aiogram.exceptions import TelegramNotFound

from bot import strings
from bot.bot_instance import bot
from bot.db.queries.users import get_user_or_none_by_id, update_user
from bot.db.queries.wishlists import get_all_parties_wishlists_in_days
from bot.keyboards.inline import wishlist_items_keyboard
from bot.utils.get_async_session import get_async_session


async def party_is_soon_message(days: int = 3):
    session = get_async_session()
    async with session.begin() as session:
        wishlists = await get_all_parties_wishlists_in_days(session, days=days)
        for wishlist in wishlists:
            owner = await get_user_or_none_by_id(session, wishlist.creator_id)
            customers_id = set()
            for item in wishlist.items:
                if item.customer_id is None:
                    continue
                customers_id.add(item.customer_id)

            customers = [await get_user_or_none_by_id(session, customer_id) for customer_id in customers_id]

            # wishlist_related_users = await get_wishlist_related_users(session, wishlist)

            for customer in customers:
                customer_items = list(filter(lambda item_: item_.customer_id == customer.id, wishlist.items))
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
                try:
                    await bot.send_message(
                        chat_id=customer.telegram_id,
                        text=text,
                        reply_markup=markup
                    )
                    await asyncio.sleep(0.04)
                except TelegramNotFound:
                    await update_user(session, user=customer, is_active=False)


