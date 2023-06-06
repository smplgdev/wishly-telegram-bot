from aiogram.fsm.state import StatesGroup, State


class ChangeName(StatesGroup):
    name = State()


class FindWishlist(StatesGroup):
    hashcode = State()


class AddItem(StatesGroup):
    title = State()
    description = State()
    link = State()
    price = State()
    photo = State()
    final = State()


class CreateWishlist(StatesGroup):
    title = State()
    expiration_date = State()
    change_name = State()
    change_date = State()
