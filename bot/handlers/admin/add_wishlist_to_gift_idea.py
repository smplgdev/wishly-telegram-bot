from aiogram import Router, types
from sqlalchemy.ext.asyncio import AsyncSession

from bot import strings
from bot.db.queries.gift_ideas import make_gift_idea_wishlist_from_wishlist
from bot.db.queries.wishlists import get_wishlist_by_id
from bot.keyboards.callback_factories import WishlistToGiftIdeaCallback

admin_router = Router()


@admin_router.callback_query(WishlistToGiftIdeaCallback.filter())
async def add_wishlist_to_gift_idea_handler(call: types.CallbackQuery,
                                            callback_data: WishlistToGiftIdeaCallback,
                                            session: AsyncSession):
    wishlist_id = callback_data.wishlist_id
    wishlist = await get_wishlist_by_id(session, wishlist_id)
    await make_gift_idea_wishlist_from_wishlist(session, wishlist)
    await call.answer(strings.wishlist_successfully_added_as_gift_ideas, show_alert=True)
