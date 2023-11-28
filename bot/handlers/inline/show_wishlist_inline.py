import random

from aiogram import Router, F, types
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent
from sqlalchemy.ext.asyncio import AsyncSession

from bot import strings, urls
from bot.db.models import Item, Wishlist, User
from bot.db.queries.users import get_user_or_none_by_id, get_user_or_none_by_telegram_id
from bot.db.queries.wishlists import get_wishlist_by_hashcode
from bot.filters.is_logged_user_filter import IsLoggedUserFilter
from bot.keyboards.inline import item_markup, wishlist_items_keyboard

router = Router()


@router.inline_query(
    F.query.regexp('^[A-Z0-9]{4}$'),
    IsLoggedUserFilter(is_logged=True)
)
async def show_wishlist_inline_handler(query: types.InlineQuery, session: AsyncSession):
    hashcode = query.query
    wishlist = await get_wishlist_by_hashcode(session=session, wishlist_hashcode=hashcode)
    if not wishlist:
        return
    items: list[Item] = wishlist.items
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query.id,
            title=strings.hide_wishlist_items,
            thumb_url=urls.EMPTY_PICTURE,
            description=None if items else strings.no_items_in_wishlist,
            input_message_content=InputTextMessageContent(
                message_text=strings.wishlist_list_was_closed
            )
        )
    )
    creator = await get_user_or_none_by_id(session, wishlist.creator_id)
    if creator.telegram_id == query.from_user.id:
        is_owner = True
    else:
        is_owner = False
    for item in items:
        results.append(InlineQueryResultArticle(
            id=str(query.id) + str(item.id),
            title=item.title if not item.customer_id else "✅ " + item.title,
            thumb_url=item.thumb_link if item.thumb_link is not None else random.choice(urls.gift_icon_links),
            description=item.description,
            input_message_content=InputTextMessageContent(
                message_text=strings.get_inline_query_message_text(
                    title=item.title,
                    description=item.description,
                    photo_link=item.photo_link
                )
            ),
            reply_markup=item_markup(
                item=item,
                wishlist_hashcode=wishlist.hashcode,
                is_owner=is_owner,
            )
        ))

    await query.answer(
        results,
        switch_pm_text=f"Вишлист «{wishlist.title}». Автор: {creator.name}",
        switch_pm_parameter=f"wl_{wishlist.hashcode}",
        cache_time=10,
        # is_personal=True
    )


# @router.inline_query(
#     F.query.regexp('^wl_[A-Z0-9]{4}$'),
# )
# async def share_wishlist_inline_query_handler(query: types.InlineQuery):
#     wishlist_hashcode = query.query.split('wl_')[-1]
#     wishlist = await WishlistCommand.get_by_hashcode(wishlist_hashcode)
#     wishlist_owner = await UserCommand.get(wishlist.creator_tg_id)
#     markup = GetInlineKeyboardMarkup.wishlist_items_keyboard(
#         wishlist_id=wishlist.id,
#         wishlist_hashcode=wishlist.hashcode,
#         is_owner=False
#     )
#     await query.answer(
#         results=[
#             InlineQueryResultArticle(
#                     id=wishlist.id,
#                     title=f"Вишлист «{wishlist.title}» #{wishlist.hashcode}",
#                     description=f"Автор: {wishlist_owner.name} 🗓 {wishlist.expiration_date.strftime('%d.%m.%Y')}",
#                     thumb_url=random.choice(links.wishlist_icon_links),
#                     input_message_content=InputTextMessageContent(
#                         message_text=strings.wishlist_detailed_information(
#                             wishlist=wishlist,
#                             wishlist_owner=wishlist_owner,
#                         ),
#                     ),
#                     reply_markup=markup,
#             )
#         ]
#     )
#
#
@router.inline_query(
    IsLoggedUserFilter(is_logged=True)
)
async def other_inline_queries_handler(query: types.InlineQuery, session: AsyncSession):
    user_telegram_id = query.from_user.id
    user = await get_user_or_none_by_telegram_id(session, user_telegram_id)
    wishlists: list[Wishlist] = user.wishlists
    results = []
    for wishlist in wishlists:
        if not wishlist.is_active:
            continue
        user: User = await get_user_or_none_by_id(session, wishlist.creator_id)
        results.append(
            InlineQueryResultArticle(
                id=str(wishlist.id),
                title=f"Вишлист «{wishlist.title}» #{wishlist.hashcode}",
                description=f"Автор: {user.name} 🗓 {wishlist.expiration_date.strftime('%d.%m.%Y')}",
                thumb_url=random.choice(urls.wishlist_icon_links),
                input_message_content=InputTextMessageContent(
                    message_text=strings.wishlist_detailed_information(
                        wishlist=wishlist,
                        wishlist_owner=user,
                    ),
                ),
                reply_markup=wishlist_items_keyboard(
                    wishlist_id=wishlist.id,
                    wishlist_hashcode=wishlist.hashcode,
                    is_owner=False
                )
            )
        )

    await query.answer(
        results=results,
        cache_time=10,
        switch_pm_text=strings.go_to_bot,
        switch_pm_parameter="go_to_bot"
    )
