from aiogram import Router, F, types


from bot import strings
from bot.filters.is_logged_user_filter import IsLoggedUserFilter
from bot.filters.is_wishlist_exists import IsWishlistExists

router = Router()


@router.inline_query(
    IsLoggedUserFilter(is_logged=False),
    IsWishlistExists(),
    F.query.regexp('^[A-Z0-9]{4}$'),
)
async def non_logged_user_inline_query_wishlist(query: types.InlineQuery):
    await query.answer(
        results=[],
        switch_pm_text=strings.first_log_in,
        switch_pm_parameter="wl_" + query.query,
        is_personal=True
    )


@router.inline_query(
    IsLoggedUserFilter(is_logged=False)
)
async def non_logged_users_inline_query_handler(query: types.InlineQuery):
    await query.answer(
        results=[],
        switch_pm_text=strings.first_log_in,
        switch_pm_parameter=query.query if query.query else "inline_query",
        is_personal=True
    )
