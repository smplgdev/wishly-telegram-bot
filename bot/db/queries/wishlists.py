import datetime
import logging
from datetime import date

from sqlalchemy import select, or_
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
                          purpose: str,
                          expiration_date: date) -> Wishlist:
    hashcode = await get_unique_hashcode(session)
    wishlist_to_create = Wishlist(
        creator_id=creator_id,
        title=title,
        purpose=purpose,
        hashcode=hashcode,
        expiration_date=expiration_date
    )
    wishlist = await session.merge(wishlist_to_create)
    await session.commit()
    logging.info("Created new wishlist – %s" % wishlist)
    return wishlist


async def get_unique_hashcode(session: AsyncSession):
    stmt = (
        select(Wishlist.hashcode)
    )
    used_hashcodes = (await session.execute(stmt)).scalars()
    while True:
        hashcode = generate_random_code(4)
        if hashcode not in used_hashcodes:
            break
    return hashcode


async def update_wishlist(session: AsyncSession, wishlist: Wishlist, **kwargs) \
        -> Wishlist | bool:
    if not wishlist:
        return False
    for key, value in kwargs.items():
        setattr(wishlist, key, value)
    await session.commit()
    return wishlist


async def make_wishlist_inactive(session: AsyncSession, wishlist: Wishlist):
    if not wishlist.is_active:
        return
    setattr(wishlist, "is_active", False)
    logging.info("Wishlist deactivated %s" % wishlist)
    await session.commit()


async def get_empty_wishlists_during_period(session: AsyncSession, days: int = 1):
    stmt = (
        select(Wishlist).
        where(Wishlist.is_active.is_(True)).
        where(Wishlist.created_at + datetime.timedelta(days=days) >= datetime.date.today())
    )

    wishlists = (await session.execute(stmt)).scalars()
    empty_wishlists = list()
    for wishlist in wishlists:
        if len(wishlist.items) == 0:
            empty_wishlists.append(wishlist)
    return empty_wishlists


async def get_all_parties_wishlists_in_days(session: AsyncSession, days: list[int]):
    today = datetime.date.today()
    expiration_days = [today + datetime.timedelta(days=day) for day in days]
    stmt = (
        select(Wishlist).
        where(Wishlist.is_active.is_(True)).
        where(or_(*[Wishlist.expiration_date == day for day in expiration_days]))
    )
    return (await session.execute(stmt)).scalars().all()


async def get_expired_wishlists(session: AsyncSession, date_: datetime.date = datetime.date.today()):
    stmt = (
        select(Wishlist).
        where(Wishlist.is_active.is_(True)).
        where(Wishlist.expiration_date + datetime.timedelta(days=1) <= date_)
    )

    return (await session.execute(stmt)).scalars().all()


async def delete_wishlist(session: AsyncSession, wishlist_id: int):
    wishlist = await get_wishlist_by_id(session, wishlist_id)
    await session.delete(wishlist)
    await session.commit()
