from aiogram.fsm.state import StatesGroup, State


class ChangeNameStates(StatesGroup):
    name = State()
