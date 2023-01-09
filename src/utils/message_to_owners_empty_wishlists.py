import asyncio

from aiogram import Bot

from database.pgcommands.commands import WishlistCommand
from keyboards.inline import GetInlineKeyboardMarkup
from src import strings


async def send_message_to_owners_of_empty_wishlists(
        bot: Bot
):
    empty_wishlists = await WishlistCommand.get_empty_wishlists_in_days(1)
    for wishlist in empty_wishlists:
        try:
            await bot.send_message(
                chat_id=wishlist.creator_tg_id,
                text=strings.your_wishlist_is_still_empty(wishlist=wishlist),
                reply_markup=GetInlineKeyboardMarkup.add_items(wishlist_id=wishlist.id)
            )
            await asyncio.sleep(0.04)
        except:
            pass
