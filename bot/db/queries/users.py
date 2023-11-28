from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import Item
from bot.db.models.users import User


async def get_user_or_none_by_telegram_id(session: AsyncSession, telegram_id: int) \
        -> User | None:
    stmt = (
        select(User).
        filter(User.telegram_id == telegram_id)
    )

    return (await session.execute(stmt)).scalar()


async def get_user_or_none_by_id(session: AsyncSession, user_id: int) \
        -> User | None:
    stmt = (
        select(User).
        filter(User.id == user_id)
    )

    return (await session.execute(stmt)).scalar()


async def check_user_exists_by_telegram_id(session: AsyncSession, telegram_id: int) \
        -> bool:
    user = await get_user_or_none_by_telegram_id(session, telegram_id)
    return user is not None


async def register_user_or_pass(session: AsyncSession, **kwargs) -> User | None:
    """
    Register user if not exists in database
    """
    is_registered_user = await check_user_exists_by_telegram_id(
        session, kwargs.get("telegram_id")
    )
    if is_registered_user:
        return None
    user = User(**kwargs)
    await session.merge(user)
    await session.commit()
    return user


async def update_user(session: AsyncSession, user: User, **kwargs) \
        -> bool:
    if not user:
        return False
    for key, value in kwargs.items():
        setattr(user, key, value)
    await session.commit()
    return True


async def gift_item(session: AsyncSession, user: User, item: Item) -> bool:
    users_items = await get_all_users_gifts(session)
    if item in users_items:
        return False
    user.items.append(item)
    await session.commit()
    return True


async def get_all_users_gifts(session: AsyncSession):
    stmt = (
        select(User.items)
    )
    return (await session.execute(stmt)).scalars()
