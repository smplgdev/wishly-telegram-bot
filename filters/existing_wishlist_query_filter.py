from aiogram.filters import BaseFilter
from aiogram.types import InlineQuery

from database.pgcommands.commands import WishlistCommand


class IsWishlistExists(BaseFilter):

    async def __call__(self, query: InlineQuery):
        wishlist_hashcode = query.query
        wishlist = await WishlistCommand.find_by_hashcode(hashcode=wishlist_hashcode)
        if wishlist:
            return True
        else:
            return False
