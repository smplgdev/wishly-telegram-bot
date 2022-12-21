from aiogram.fsm.state import StatesGroup, State


class CreateWishlist(StatesGroup):
    title = State()
    expiration_date = State()
    change_name = State()
    change_date = State()
