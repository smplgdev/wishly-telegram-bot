from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from database.models.Wishlist import Wishlist
from database.pgcommands.commands import WishlistCommand, ItemCommand, UserCommand
from keyboards.callback_factories import WishlistCallback, ItemCallback
from keyboards.inline import GetInlineKeyboardMarkup
import strings

router = Router()


@router.callback_query(WishlistCallback.filter(F.action.in_(["show", "go_back"])))
async def show_wishlist_handler(call: types.CallbackQuery, callback_data: WishlistCallback):
    await call.answer(cache_time=5)
    wishlist_id = callback_data.wishlist_id
    wishlist = await WishlistCommand.get(wishlist_id)
    await show_wishlist(
        message=call.message,
        user_id=call.from_user.id,
        wishlist=wishlist,
        show_hide_wishlist_button=True
    )


async def show_wishlist(
        message: types.Message,
        user_id: int,
        wishlist: Wishlist,
        show_hide_wishlist_button: bool = False
):
    """
    Shows selected wishlist description and button that shows gifts. If owner: also edit wishlist button
    """
    owner = await UserCommand.get(wishlist.creator_tg_id)
    if owner.tg_id == user_id:
        is_owner = True
        show_hide_wishlist_button = False
    else:
        is_owner = False
    markup = GetInlineKeyboardMarkup.list_wishlist_items(
        wishlist_id=wishlist.id,
        wishlist_hashcode=wishlist.hashcode,
        show_hide_wishlist_button=show_hide_wishlist_button,
        is_owner=is_owner
    )

    text = strings.wishlist_detailed_information(wishlist, owner)
    await message.answer(text, reply_markup=markup)


@router.message(Command('my_wishlists'))
@router.message(F.text == strings.my_wishlists)
async def show_user_wishlists(message: types.Message, state: FSMContext):
    """
    List all user's wishlists
    """
    await state.clear()
    user_wishlists = await WishlistCommand.get_all_user_wishlists(message.from_user.id)
    markup = GetInlineKeyboardMarkup.list_user_wishlists(user_wishlists)
    await message.answer(strings.your_wishlists, reply_markup=markup)


@router.callback_query(ItemCallback.filter(F.action == 'show'))
async def show_item(call: types.CallbackQuery, callback_data: ItemCallback):
    item_id = callback_data.item_id
    item = await ItemCommand.get(item_id)
    text = strings.item_info_text(title=item.title, description=item.description)
    wishlist = await WishlistCommand.get(item.wishlist_id)
    if wishlist.creator_tg_id == call.from_user.id:
        is_owner = True
    else:
        is_owner = False

    markup = GetInlineKeyboardMarkup.item_markup(
        item=item,
        wishlist_hashcode=wishlist.wishlist_hashcode,
        is_owner=is_owner
    )

    if item.photo_file_id is None:
        await call.message.edit_text(text, reply_markup=markup)
    else:
        await call.message.answer_photo(item.photo_file_id, caption=text, reply_markup=markup)
    await call.answer(cache_time=5)
