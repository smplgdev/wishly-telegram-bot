from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import SecretList
from bot.db.queries.wishlists import get_unique_hashcode


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
