from aiogram.filters import BaseFilter
from aiogram.types import InlineQuery


class ChatWithBot(BaseFilter):
    def __init__(self, is_with_bot: bool):
        self.is_with_bot = is_with_bot

    async def __call__(self, query: InlineQuery) -> bool:
        if self.is_with_bot:
            return query.chat_type == 'sender'
        else:
            return query.chat_type != 'sender'
