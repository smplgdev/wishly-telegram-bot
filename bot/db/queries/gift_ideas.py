import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import Item, Wishlist
from bot.db.models.gift_ideas import GiftIdea
from bot.db.models.gift_ideas_categories import GiftIdeaCategory


async def get_category_by_id(session: AsyncSession, category_id: int) -> GiftIdeaCategory:
    stmt = (
        select(GiftIdeaCategory).
        where(GiftIdeaCategory.id == category_id)
    )

    return (await session.execute(stmt)).scalar()


async def get_gift_idea_by_id(session: AsyncSession, gift_idea_id: int) -> GiftIdea:
    stmt = (
        select(GiftIdea).
        where(GiftIdea.id == gift_idea_id)
    )

    return (await session.execute(stmt)).scalar()


async def get_all_gift_ideas_categories(session: AsyncSession):
    stmt = (
        select(GiftIdeaCategory)
    )

    return (await session.execute(stmt)).scalars()


async def get_gift_idea_category(session: AsyncSession, category_id: int):
    stmt = (
        select(GiftIdeaCategory).
        where(GiftIdeaCategory.id == category_id)
    )
    return (await session.execute(stmt)).scalar()


async def add_gift_idea_to_wishlist(session: AsyncSession,
                                    gift_idea: GiftIdea,
                                    wishlist_id: int) -> Item:
    item = Item(
        wishlist_id=wishlist_id,
        title=gift_idea.title,
        description=gift_idea.description,
        photo_link=gift_idea.photo_link,
        price=gift_idea.price,
        photo_file_id=gift_idea.photo_file_id,
        thumb_link=gift_idea.thumb_link
    )

    item = await session.merge(item)
    await session.commit()
    logging.info("Gift idea added to wishlist\n%s" % item)
    return item


async def make_gift_idea_wishlist_from_wishlist(
        session: AsyncSession,
        wishlist: Wishlist
):
    wishlist_items: list[Item] = wishlist.items
    gift_idea = GiftIdeaCategory(
        name=wishlist.title,
    )

    gift_idea = await session.merge(gift_idea)
    for item in wishlist_items:
        gift = GiftIdea(
            gift_idea_category_id=gift_idea.id,
            title=item.title,
            description=item.description,
            photo_link=item.photo_link,
            price=item.price,
            photo_file_id=item.photo_file_id,
            thumb_link=item.thumb_link
        )
        await session.merge(gift)
    await session.commit()
