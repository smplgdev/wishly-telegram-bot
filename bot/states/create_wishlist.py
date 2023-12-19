from aiogram.fsm.state import StatesGroup, State


class CreateWishlistStates(StatesGroup):
    purpose = State()
    title = State()
    expiration_date = State()
    user_age = State()


class EditWishlistSettingsStates(StatesGroup):
    change_name = State()
    change_date = State()
