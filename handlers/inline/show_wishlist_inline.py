from aiogram import Router, F, types
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent
from aiogram.utils.markdown import hide_link

from database.pgcommands.commands import WishlistCommand, ItemCommand, UserCommand
from filters.non_logged_users import NonLoggedUserFilter
from keyboards.inline import GetInlineKeyboardMarkup
from src import links, strings

router = Router()


@router.inline_query(
    NonLoggedUserFilter()
)
async def non_logged_users_inline_query_handler(query: types.InlineQuery):
    await query.answer(
        results=[],
        switch_pm_text=strings.first_log_in,
        switch_pm_parameter=query.query if query.query else "inline_query",
        is_personal=True
    )


@router.inline_query(
    F.query.regexp('^[A-Z0-9]{4}$'),
    # ChatWithBot(is_with_bot=True)
)
async def show_wishlist_inline_handler(query: types.InlineQuery):
    def get_message_text(
            title: str,
            description: str,
            photo_link: str
    ) -> str:
        text_parts = list()

        text_parts.append(
            f"<b>{title}</b>" + hide_link(photo_link)
        )
        if description:
            text_parts.append(
                "\n" + description
            )
        return '\n'.join(text_parts)

    hashcode = query.query
    wishlist = await WishlistCommand.find_by_hashcode(hashcode)
    if not wishlist:
        return
    items = await ItemCommand.get_all_wishlist_items(wishlist.id)
    results = []

    for item in items:
        results.append(InlineQueryResultArticle(
            id=item.id,
            title=item.title if not item.buyer_tg_id else "✅ " + item.title,
            thumb_url=item.thumb_link if item.thumb_link is not None else links.gift_icon_link,
            # description=item.description,
            input_message_content=InputTextMessageContent(
                message_text=get_message_text(
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
