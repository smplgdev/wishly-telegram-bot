from aiogram.fsm.state import StatesGroup, State


class AddItemStates(StatesGroup):
    title = State()
    description = State()
    link = State()
    price = State()
    photo = State()
    final = State()
