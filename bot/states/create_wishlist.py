from aiogram.fsm.state import StatesGroup, State


class CreateWishlistStates(StatesGroup):
    title = State()
    expiration_date = State()


class EditWishlistSettingsStates(StatesGroup):
    change_name = State()
    change_date = State()
