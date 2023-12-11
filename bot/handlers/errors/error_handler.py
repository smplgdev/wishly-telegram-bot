import logging

from aiogram import Router, F
from aiogram.types import ErrorEvent, Message

from bot import strings

router = Router()


@router.error(F.update.message.as_("message"))
async def error_handler(event: ErrorEvent, message: Message):
    logging.error("Critical error caused by %s", event.exception, exc_info=True)

    await message.answer(strings.error_happened)
