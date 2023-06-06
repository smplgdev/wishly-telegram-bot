from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from database.pgcommands.commands import UserCommand
from keyboards.default import GetKeyboardMarkup
import strings
from states.change_name import ChangeName

router = Router()


@router.message(Command('name'))
@router.message(F.text.contains(strings.change_visible_name))
async def settings_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await state.set_state(ChangeName.name)
    await message.answer(strings.send_new_name)


@router.message(ChangeName.name)
async def change_name_handler(message: types.Message, state: FSMContext):
    new_name = message.text
    if len(new_name) > 64:
        await message.answer(strings.name_too_long)
        return
    await UserCommand.update_name(message.from_user.id, new_name)
    markup = GetKeyboardMarkup.start(new_name)
    await state.clear()
    await message.answer(strings.name_successfully_changed,
                         reply_markup=markup)
