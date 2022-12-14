from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, InlineQuery
from typing import Union

from database.pgcommands.commands import UserCommand


class NonLoggedUserFilter(BaseFilter):

    async def __call__(self, query: Union[CallbackQuery, InlineQuery]) -> bool:
        user = await UserCommand.get(query.from_user.id)
        if user:
            return False
        return True
