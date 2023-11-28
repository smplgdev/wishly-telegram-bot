from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.filters import CommandObject
from aiogram.types import TelegramObject, Message, CallbackQuery

from bot.db.queries.users import get_user_or_none_by_telegram_id, update_user, register_user_or_pass


class UpdateUserDataMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any],
    ):
        session = data["session"]
        if isinstance(event, Message):
            telegram_id = event.from_user.id
            name = event.from_user.first_name
            username = event.from_user.username
        elif isinstance(event, CallbackQuery):
            telegram_id = event.from_user.id
            name = event.from_user.first_name
            username = event.from_user.username
        else:
            return await handler(event, data)
        user = await get_user_or_none_by_telegram_id(session, telegram_id=telegram_id)
        if user:
            await update_user(
                session,
                user=user,
                name=name,
                username=username,
                is_active=True,
            )
        else:
            deep_link = None
            if "command" in data.keys():
                command: CommandObject = data["command"]
                deep_link = command.args
            user = await register_user_or_pass(
                session,
                telegram_id=telegram_id,
                name=name,
                username=username,
                deep_link=deep_link
            )
        data["user"] = user
        return await handler(event, data)
