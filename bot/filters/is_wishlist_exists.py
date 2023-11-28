from aiogram.filters import BaseFilter
from aiogram.types import InlineQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.queries.wishlists import get_wishlist_by_hashcode


class IsWishlistExists(BaseFilter):

    async def __call__(self, query: InlineQuery, session: AsyncSession):
        wishlist_hashcode = query.query
        wishlist = await get_wishlist_by_hashcode(session, wishlist_hashcode)
        if wishlist:
            return True
        else:
            return False
