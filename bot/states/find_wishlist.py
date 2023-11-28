from aiogram.fsm.state import StatesGroup, State


class FindWishlistStates(StatesGroup):
    hashcode = State()
