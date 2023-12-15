from aiogram.fsm.state import StatesGroup, State


class CreateSecretListStates(StatesGroup):
    title = State()
    expiration_date = State()
    max_participants = State()
    gift_limit = State()
