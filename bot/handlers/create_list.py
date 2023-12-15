from aiogram import Bot
from aiogram.fsm.context import FSMContext

from bot import strings
from bot.states.create_secret_list import CreateSecretListStates
from bot.states.create_wishlist import CreateWishlistStates
from bot.utils.types import ListTypes


async def create_list(
        bot: Bot,
        user_id: int,
        list_type: ListTypes,
        state: FSMContext,
):
    await state.clear()
    if list_type == ListTypes.WISHLIST:
        text = strings.enter_wishlist_title
        state_to_set = CreateWishlistStates.title
    elif list_type == ListTypes.SECRET_LIST:
        text = strings.enter_secret_list_title
        state_to_set = CreateSecretListStates.title
    else:
        return

    await state.set_state(state_to_set)

    await bot.send_message(
        chat_id=user_id,
        text=text,
    )
