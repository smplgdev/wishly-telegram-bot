from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger


def set_scheduled_jobs(
        scheduler: AsyncIOScheduler,
        bot: Bot,
        *args,
        **kwargs,
):
    return
    scheduler.add_job(week_before_party, CronTrigger(hour=7, minute=2), args=(bot,))
    scheduler.add_job(send_messages_to_wishlists_owner, CronTrigger(hour=14, minute=30), args=(bot,))
    scheduler.add_job(send_message_to_owners_of_empty_wishlists, CronTrigger(hour=13, minute=0), args=(bot,))


async def send_message_to_owners_of_empty_wishlists(
        bot: Bot
):
    empty_wishlists = await get_empty_wishlists_since_create(1)
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


async def week_before_party(bot: Bot):
    wishlists = await WishlistCommand.get_all_parties_wishlists_in_days(7)
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
            markup = GetInlineKeyboardMarkup.wishlist_items_keyboard(
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


async def send_messages_to_wishlists_owner(bot: Bot):
    wishlists = await WishlistCommand.get_all_parties_wishlists_in_days(7)
    for wishlist in wishlists:
        owner = await UserCommand.get(wishlist.creator_tg_id)
        related_users = await WishlistCommand.get_all_related_users(wishlist_id=wishlist.id)
        items = await ItemCommand.get_all_wishlist_items(wishlist_id=wishlist.id)
        gifted_items = list(filter(lambda i: i.buyer_tg_id, items))
        non_gifted_items = list(filter(lambda i: not i.buyer_tg_id, items))
        text = strings.wishlist_owner_party_soon(
            owner=owner,
            wishlist=wishlist,
            related_users=related_users,
            gifted_items=gifted_items,
            non_gifted_items=non_gifted_items,
        )
        try:
            await bot.send_message(
                chat_id=owner.tg_id,
                text=text
            )
            await asyncio.sleep(0.04)
        except Exception as e:
            print(e)
            await UserCommand.make_inactive(user_tg_id=owner.tg_id)
