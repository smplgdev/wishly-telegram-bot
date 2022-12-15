from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, InlineQuery
from typing import Union

from database.pgcommands.commands import UserCommand


class IsLoggedUserFilter(BaseFilter):
    def __init__(self, is_logged: bool):
        self.is_logged = is_logged

    async def __call__(self, query: Union[CallbackQuery, InlineQuery]) -> bool:
        user = await UserCommand.get(query.from_user.id)
        if user:
            return self.is_logged is True
        else:
            return self.is_logged is False
