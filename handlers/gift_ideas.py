from aiogram import Router, types, F

from src import strings

router = Router()


@router.message(F.text == strings.gift_ideas)
async def gift_ideas_handler(message: types.Message):
    await message.reply("Этот раздел пока что находится в разработке :(")
