import asyncio

from aiogram import Bot

from database.pgcommands.commands import WishlistCommand, UserCommand, ItemCommand
from keyboards.inline import GetInlineKeyboardMarkup
from src import strings


async def week_before_party(bot: Bot):
    wishlists = await WishlistCommand.get_all_parties_wishlists_in_week()
    counter = 0
    for wishlist in wishlists:
        owner = await UserCommand.get(user_tg_id=wishlist.creator_tg_id)
        items = await ItemCommand.get_all_wishlist_items(wishlist_id=wishlist.id)
        givers: dict[int, list | None] = {}
        for item in items:
            if item.buyer_tg_id is not None:
                if item.buyer_tg_id in givers.keys():
                    givers[item.buyer_tg_id].append(item)
                else:
                    givers[item.buyer_tg_id] = [item]

        all_related_users = await WishlistCommand.get_all_related_users(wishlist_id=wishlist.id)

        for user in all_related_users:
            if user.tg_id in givers.keys():
                continue
            givers[user.tg_id] = None

        for giver_tg_id, items in givers.items():
            text = strings.party_soon(
                wishlist=wishlist,
                owner=owner,
                items=items
            )
            markup = GetInlineKeyboardMarkup.list_wishlist_items(
                wishlist_id=wishlist.id,
                wishlist_hashcode=wishlist.hashcode,
                show_hide_wishlist_button=False,
                is_owner=False
            )
            try:
                await bot.send_message(
                    chat_id=giver_tg_id,
                    text=text,
                    reply_markup=markup
                )
                await asyncio.sleep(0.04)
            except Exception as e:
                print(e)
                counter += 1
                await UserCommand.make_inactive(user_tg_id=giver_tg_id)

