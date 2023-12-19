import logging

from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import Item


async def get_item_by_id(session: AsyncSession, item_id: int) -> Item | None:
    stmt = (
        select(Item).
        filter(Item.id == item_id)
    )
    return (await session.execute(stmt)).scalar()


async def add_item_to_wishlist(
        session: AsyncSession, wishlist_id: int,
        photo_link: str | None,
        title: str, description: str | None,
        photo_file_id: str | None, **kwargs) -> Item:
    item_to_create = Item(
        wishlist_id=wishlist_id,
        title=title,
        description=description,
        photo_link=photo_link,
        photo_file_id=photo_file_id,
        **kwargs
    )
    item = await session.merge(item_to_create)
    await session.commit()
    logging.info("New item added %s" % item)
    return item


async def count_items_in_wishlist(session: AsyncSession, wishlist_id: int):
    stmt = (
        select(func.count()).
        where(Item.wishlist_id == wishlist_id).
        select_from(Item)
    )

    return (await session.execute(stmt)).scalar()


async def delete_item(session: AsyncSession, item: Item):
    await session.delete(item)
    await session.commit()


async def update_item(session: AsyncSession, item: Item, **kwargs):
    if not item:
        return False
    for key, value in kwargs.items():
        setattr(item, key, value)
    await session.commit()
