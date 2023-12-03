import datetime

from bot.db.queries.wishlists import get_expired_wishlists, make_wishlist_inactive
from bot.utils.get_async_session import get_async_session


async def make_old_wishlists_inactive(date_: datetime.date = datetime.date.today()):
    async with get_async_session().begin() as session:
        expired_wishlists = await get_expired_wishlists(session, date_)
        for wishlist in expired_wishlists:
            await make_wishlist_inactive(session, wishlist)
