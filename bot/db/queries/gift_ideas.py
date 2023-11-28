from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import Item
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


async def get_all_gifts_from_category(session: AsyncSession, category_id: int):
    stmt = (
        select(GiftIdea).
        where(GiftIdea.gift_idea_category_id == category_id)
    )

    return (await session.execute(stmt)).scalars()


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
    return item
