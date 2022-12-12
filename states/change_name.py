from aiogram.fsm.state import StatesGroup, State


class ChangeName(StatesGroup):
    name = State()
