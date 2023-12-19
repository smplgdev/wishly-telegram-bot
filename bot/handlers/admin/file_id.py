from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

admin_router = Router()


@admin_router.message(F.content_type.in_('photo'), Command('file_id'))
async def send_photo_file_id(message: Message):
    await message.reply(message.photo[-1].file_id)
