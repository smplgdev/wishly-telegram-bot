import random

from aiogram import Router, F, types
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent

from database.pgcommands.commands import WishlistCommand, ItemCommand, UserCommand
from filters.existing_wishlist_query_filter import IsWishlistExists
from filters.is_logged_user import IsLoggedUserFilter
from keyboards.inline import GetInlineKeyboardMarkup
from src import links, strings

router = Router()


@router.inline_query(
    F.query.regexp('^[A-Z0-9]{4}$'),
    IsWishlistExists(),
    IsLoggedUserFilter(is_logged=True)
)
async def show_wishlist_inline_handler(query: types.InlineQuery):
    hashcode = query.query
    wishlist = await WishlistCommand.find_by_hashcode(hashcode)

    items = await ItemCommand.get_all_wishlist_items(wishlist.id)
    results = []

    for item in items:
        results.append(InlineQueryResultArticle(
            id=item.id,
            title=item.title if not item.buyer_tg_id else "✅ " + item.title,
            thumb_url=item.thumb_link if item.thumb_link is not None else random.choice(links.gift_icon_links),
            description=item.description,
            input_message_content=InputTextMessageContent(
                message_text=strings.get_inline_query_message_text(
                    title=item.title,
                    description=item.description,
                    photo_link=item.photo_link
                )
            ),
            reply_markup=GetInlineKeyboardMarkup.item_markup(
                item=item,
                wishlist_hashcode=wishlist.hashcode,
                is_owner=False,
            )
        ))

    user = await UserCommand.get(wishlist.creator_tg_id)

    await query.answer(
        results,
        switch_pm_text=f"Вишлист «{wishlist.title}». Автор: {user.name}",
        switch_pm_parameter=f"wl_{wishlist.hashcode}",
        is_personal=True
    )


@router.inline_query(
    F.query.regexp('^wl_[A-Z0-9]{4}$'),
)
async def share_wishlist_inline_query_handler(query: types.InlineQuery):
    wishlist_hashcode = query.query.split('wl_')[-1]
    wishlist = await WishlistCommand.get_by_hashcode(wishlist_hashcode)
    wishlist_owner = await UserCommand.get(wishlist.creator_tg_id)
    markup = GetInlineKeyboardMarkup.list_wishlist_items(
        wishlist_id=wishlist.id,
        wishlist_hashcode=wishlist.hashcode,
        is_owner=False
    )
    await query.answer(
        results=[
            InlineQueryResultArticle(
                    id=wishlist.id,
                    title=f"Вишлист «{wishlist.title}»",
                    description=f"Автор: {wishlist_owner.name} 🗓 {wishlist.expiration_date.strftime('%d.%m.%Y')}",
                    thumb_url=random.choice(links.wishlist_icon_links),
                    input_message_content=InputTextMessageContent(
                        message_text=strings.wishlist_title(
                            wishlist=wishlist,
                            wishlist_owner=wishlist_owner,
                        ),
                    ),
                    reply_markup=markup,
            )
        ]
    )


@router.inline_query(
    IsLoggedUserFilter(is_logged=True)
)
async def other_inline_queries_handler(query: types.InlineQuery):
    user_tg_id = query.from_user.id
    wishlists = await WishlistCommand.get_related_wishlists(
        user_tg_id=user_tg_id,
    )
    results = []
    for wishlist in wishlists:
        wishlist_owner = await UserCommand.get(user_tg_id=wishlist.creator_tg_id)
        results.append(
            InlineQueryResultArticle(
                id=wishlist.id,
                title=f"Вишлист «{wishlist.title}»",
                description=f"Автор: {wishlist_owner.name} 🗓 {wishlist.expiration_date.strftime('%d.%m.%Y')}",
                thumb_url=random.choice(links.wishlist_icon_links),
                input_message_content=InputTextMessageContent(
                    message_text=strings.wishlist_title(
                        wishlist=wishlist,
                        wishlist_owner=wishlist_owner,
                    ),
                ),
                reply_markup=GetInlineKeyboardMarkup.list_wishlist_items(
                    wishlist_id=wishlist.id,
                    wishlist_hashcode=wishlist.hashcode,
                    is_owner=False
                )
            )
        )

    await query.answer(
        results=results,
        is_personal=True,
        switch_pm_text=strings.go_to_bot,
        switch_pm_parameter="go_to_bot"
    )
