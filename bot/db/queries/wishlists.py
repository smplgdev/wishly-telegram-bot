import datetime
from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.operators import and_

from bot.db.models import Wishlist, User, wishlist_user_association
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


async def make_wishlist_inactive(session: AsyncSession, wishlist: Wishlist):
    if not wishlist.is_active:
        return
    setattr(wishlist, "is_active", False)
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


async def get_all_parties_wishlists_in_days(session: AsyncSession, days: int = 5):
    today = datetime.date.today()
    stmt = (
        select(Wishlist).
        where(Wishlist.is_active.is_(True)).
        where(today + datetime.timedelta(days=days) == Wishlist.expiration_date)
    )
    return (await session.execute(stmt)).scalars()


async def get_expired_wishlists(session: AsyncSession, date_: datetime.date = datetime.date.today()):
    stmt = (
        select(Wishlist).
        where(Wishlist.expiration_date + datetime.timedelta(days=1) <= date_)
    )

    return (await session.execute(stmt)).scalars()


async def get_wishlist_related_users(session: AsyncSession, wishlist_id: int):
    stmt = (
        select(User).
        join(wishlist_user_association).
        filter(wishlist_user_association.c.wishlist_id == wishlist_id)
    )

    return (await session.execute(stmt)).scalars()


async def delete_wishlist(session: AsyncSession, wishlist_id: int):
    wishlist = await get_wishlist_by_id(session, wishlist_id)
    await session.delete(wishlist)
    await session.commit()
