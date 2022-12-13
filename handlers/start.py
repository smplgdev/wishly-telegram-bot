import io

from aiogram import Router, F, types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database.pgcommands.commands import UserCommand, WishlistCommand
from keyboards.default import GetKeyboardMarkup
from keyboards.inline import GetInlineKeyboardMarkup
from src import strings

router = Router()


@router.message(Command('home'))
@router.message(Command('help'))
@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    deep_link = get_deep_link(message.text)
    user_tg_id = message.from_user.id
    user = await UserCommand.add(tg_id=user_tg_id,
                                 name=message.from_user.first_name,
                                 deep_link=deep_link,
                                 username=message.from_user.username)
    greet_message = strings.start_text(message.from_user.first_name)
    await message.answer(greet_message, reply_markup=GetKeyboardMarkup.start(user.name))
    if deep_link:
        hashcode = deep_link
        wishlist = await WishlistCommand.get_by_hashcode(hashcode)
        creator_user = await UserCommand.get(wishlist.creator_tg_id)
        wishlist_found_text = strings.wishlist_found_in_deep_link(
            wishlist=wishlist,
            creator_user=creator_user)
        await message.answer(wishlist_found_text,
                             reply_markup=GetInlineKeyboardMarkup.go_to_wishlist(wishlist.id))


def get_deep_link(message_text: str):
    m = message_text.split("wl_")
    if len(m) > 1 and m[-1]:
        return m[-1]
    return None
