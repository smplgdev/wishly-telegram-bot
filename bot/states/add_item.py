from aiogram.fsm.state import StatesGroup, State


class AddItemStates(StatesGroup):
    purpose = State()
    title = State()
    description = State()
    link = State()
    price = State()
    photo = State()
    final = State()
