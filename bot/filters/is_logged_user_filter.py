from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import InlineQuery, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.queries.users import get_user_or_none_by_telegram_id


class IsLoggedUserFilter(BaseFilter):
    def __init__(self, is_logged: bool):
        self.is_logged = is_logged

    async def __call__(self, query: Union[CallbackQuery, InlineQuery], session: AsyncSession) -> bool:
        user = await get_user_or_none_by_telegram_id(session, query.from_user.id)
        if user:
            return self.is_logged is True
        else:
            return self.is_logged is False
