import random
import re

from aiogram import Router, F, types
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent
from sqlalchemy.ext.asyncio import AsyncSession

from bot import strings, urls
from bot.db.queries.gift_ideas import get_gift_idea_category
from bot.filters.is_logged_user_filter import IsLoggedUserFilter
from bot.keyboards.inline import get_gift_idea_keyboard

router = Router()


@router.inline_query(
    F.query.regexp(r'^ideas_\d+$'),
    IsLoggedUserFilter(is_logged=True)
)
async def show_gift_ideas_handler(query: types.InlineQuery, session: AsyncSession):
    gift_idea_category_id = re.search(r"\d+", query.query)[0]
    if not gift_idea_category_id:
        return
    else:
        gift_idea_category_id = int(gift_idea_category_id)
    gift_idea_category = await get_gift_idea_category(session, gift_idea_category_id)
    gift_ideas = gift_idea_category.gift_ideas
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query.id,
            title=strings.hide_gift_ideas,
            thumb_url=urls.EMPTY_PICTURE,
            description=None if len(gift_ideas) > 0 else strings.no_items_in_wishlist,
            input_message_content=InputTextMessageContent(
                message_text=strings.wishlist_list_was_closed
            )
        )
    )
    for gift in gift_ideas:
        results.append(
            InlineQueryResultArticle(
                id=str(query.id) + str(gift.id),
                title=gift.title,
                thumb_url=gift.thumb_link if gift.thumb_link is not None else random.choice(urls.gift_icon_links),
                description=gift.description,
                input_message_content=InputTextMessageContent(
                    message_text=strings.get_inline_query_message_text(
                        title=gift.title,
                        description=gift.description,
                        photo_link=gift.photo_link
                    )
                ),
                reply_markup=get_gift_idea_keyboard(
                    gift_idea=gift,
                    gift_idea_category=gift_idea_category,
                )
            )
        )
    await query.answer(
        results,
        cache_time=300,
    )
