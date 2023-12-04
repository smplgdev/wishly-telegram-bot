import logging

from aiogram import Router
from aiogram.types import ErrorEvent

from bot import strings

router = Router()


@router.error()
async def error_handler(event: ErrorEvent):
    logging.error("Critical error caused by %s", event.exception, exc_info=True)

    await event.update.message.answer(strings.error_happened)
