from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import Message, InlineQuery

from bot.config_reader import config

ADMINS = config.ADMINS


class AdminFilter(BaseFilter):
    def __init__(self, is_admin: bool = True):
        self.is_admin = is_admin

    async def __call__(self, message: Message):
        if not self.is_admin:
            return message.from_user.id not in ADMINS
        return message.from_user.id in ADMINS


class ChatTypeFilter(BaseFilter):
    def __init__(self, is_group: bool):
        self.is_group = is_group

    async def __call__(self, message: Message) -> bool:
        if self.is_group:
            return message.chat.type in ['group', 'supergroup']
        else:
            return message.chat.type == 'private'


class ChatTypeFilterInlineQuery(BaseFilter):
    def __init__(self, chat_type: Union[str, list]):
        self.chat_type = chat_type

    async def __call__(self, query: InlineQuery) -> bool:
        if isinstance(self.chat_type, str):
            return query.chat_type == self.chat_type
        else:
            return query.chat_type in self.chat_type


class ChatWithBot(BaseFilter):
    def __init__(self, is_with_bot: bool):
        self.is_with_bot = is_with_bot

    async def __call__(self, query: InlineQuery) -> bool:
        if self.is_with_bot:
            return query.chat_type == 'sender'
        else:
            return query.chat_type != 'sender'


class IsWishlistExists(BaseFilter):

    async def __call__(self, query: InlineQuery):
        wishlist_hashcode = query.query
        wishlist = await WishlistCommand.find_by_hashcode(hashcode=wishlist_hashcode)
        if wishlist:
            return True
        else:
            return False


class IsLoggedUserFilter(BaseFilter):
    def __init__(self, is_logged: bool):
        self.is_logged = is_logged

    async def __call__(self, query: Union[CallbackQuery, InlineQuery]) -> bool:
        user = await UserCommand.get(query.from_user.id)
        if user:
            return self.is_logged is True
        else:
            return self.is_logged is False
