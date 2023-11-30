from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.operators import and_

from bot.db.models import Wishlist, User
from bot.utils.random_code_generator import generate_random_code


async def get_wishlist_by_hashcode(session: AsyncSession, wishlist_hashcode: str) \
        -> Wishlist | None:
    stmt = (
        select(Wishlist).
        where(and_(
            Wishlist.hashcode == wishlist_hashcode,
            Wishlist.is_active.is_(True)
        ))
    )

    return (await session.execute(stmt)).scalar()


async def get_wishlist_by_id(session: AsyncSession, wishlist_id: int) -> Wishlist | None:
    stmt = (
        select(Wishlist).
        where(Wishlist.id == wishlist_id)
    )

    return (await session.execute(stmt)).scalar()


async def add_wishlist_to_favourite(session: AsyncSession, user: User, wishlist: Wishlist) \
        -> bool:
    if wishlist not in user.wishlists:
        user.wishlists.append(wishlist)
    await session.commit()
    return True


async def create_wishlist(session: AsyncSession,
                          creator_id: int,
                          title: str,
                          expiration_date: date):
    stmt = (
        select(Wishlist.hashcode)
    )
    used_hashcodes = (await session.execute(stmt)).scalars()
    while True:
        hashcode = generate_random_code(4)
        if hashcode not in used_hashcodes:
            break
    wishlist_to_create = Wishlist(
        creator_id=creator_id,
        title=title,
        hashcode=hashcode,
        expiration_date=expiration_date
    )
    wishlist = await session.merge(wishlist_to_create)
    await session.commit()
    return wishlist


async def update_wishlist(session: AsyncSession, wishlist: Wishlist, **kwargs) \
        -> Wishlist | bool:
    if not wishlist:
        return False
    for key, value in kwargs.items():
        setattr(wishlist, key, value)
    await session.commit()
    return wishlist
