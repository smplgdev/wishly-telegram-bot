from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import SecretList, Wishlist
from bot.db.models.secret_list_items import SecretListItem
from bot.db.models.secret_list_participants import SecretListParticipant
from bot.db.queries.users import update_user
from bot.db.queries.wishlists import get_unique_hashcode


async def add_participant(session: AsyncSession, sl_id: int, user_id: int):
    participant = SecretListParticipant(
        user_id=user_id,
        secret_list_id=sl_id
    )

    participant = await session.merge(participant)
    await session.commit()
    return participant


async def create_wishlist_for_secret_list_participant(
        session: AsyncSession,
        creator_id: int,
        participant_id: int,
        expiration_date: date,
):
    hashcode = await get_unique_hashcode(session)
    wishlist_to_create = Wishlist(
        creator_id=creator_id,
        participant_id=participant_id,
        title="Вишлист для ТС",
        hashcode=hashcode,
        expiration_date=expiration_date
    )
    wishlist = await session.merge(wishlist_to_create)
    await session.commit()
    return wishlist


async def delete_participant(session: AsyncSession, participant: SecretListParticipant):
    await session.delete(participant)
    await update_user(session, participant.user, is_active=False)
    await session.commit()


async def update_participant(session: AsyncSession, participant: SecretListParticipant, **kwargs):
    for key, value in kwargs.items():
        setattr(participant, key, value)
    await session.commit()


async def change_secret_list_status(session: AsyncSession, sl: SecretList, status: str):
    setattr(sl, "status", status)
    await session.commit()


async def get_user_secret_lists(session: AsyncSession, user_id: int):
    stmt = (
        select(SecretList).
        where(SecretList.creator_id == user_id).
        where(SecretList.status.in_(["waiting", "running"]))
    )

    return (await session.execute(stmt)).scalars().all()


async def get_participant_or_none_by_id(session: AsyncSession, participant_id: int):
    stmt = (
        select(SecretListParticipant).
        where(SecretListParticipant.id == participant_id)
    )

    return (await session.execute(stmt)).scalar()


async def create_secret_list(
        session: AsyncSession,
        creator_id: int,
        title: str,
        expiration_date: date,
        max_participants: int,
        max_gifts: int = 3,
) -> SecretList:
    hashcode = await get_unique_hashcode(session)
    secret_list_to_create = SecretList(
        creator_id=creator_id,
        title=title,
        hashcode=hashcode,
        expiration_date=expiration_date,
        max_participants=max_participants,
        max_gifts=max_gifts
    )

    secret_list = await session.merge(secret_list_to_create)
    await session.commit()
    return secret_list


async def get_secret_list_or_none_by_hashcode(session: AsyncSession, hashcode: str) -> SecretList:
    stmt = (
        select(SecretList).
        where(SecretList.hashcode == hashcode).
        where(SecretList.is_active.is_(True))
    )

    return (await session.execute(stmt)).scalar()


async def get_secret_list_or_none_by_id(session: AsyncSession, sl_id: int) -> SecretList:
    stmt = (
        select(SecretList).
        where(SecretList.id == sl_id)
    )
    return (await session.execute(stmt)).scalar()


async def add_item_to_secret_list(
        session: AsyncSession,
        participant_id: int,
        title: str,
        description: str,
        photo_link: str,
        photo_file_id: str,
        **kwargs
):
    item_to_create = SecretListItem(
        participant_id=participant_id,
        title=title,
        description=description,
        photo_link=photo_link,
        photo_file_id=photo_file_id,
        **kwargs
    )
    item = await session.merge(item_to_create)
    await session.commit()
    return item
