from aiogram.fsm.state import StatesGroup, State


class FindWishlist(StatesGroup):
    hashcode = State()

