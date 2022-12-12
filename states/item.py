from aiogram.fsm.state import StatesGroup, State


class AddItem(StatesGroup):
    title = State()
    description = State()
    link = State()
    price = State()
    photo = State()
    final = State()
