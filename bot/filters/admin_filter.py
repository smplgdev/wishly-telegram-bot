from aiogram.filters import BaseFilter
from aiogram.types import Message

from bot.filters import ADMINS


class AdminFilter(BaseFilter):
    def __init__(self, is_admin: bool = True):
        self.is_admin = is_admin

    async def __call__(self, message: Message):
        if not self.is_admin:
            return message.from_user.id not in ADMINS
        return message.from_user.id in ADMINS
