from aiogram import Router, F, types
from aiogram.filters import Command

from database.models.Wishlist import Wishlist
from database.pgcommands.commands import WishlistCommand, ItemCommand, UserCommand
from keyboards.callback_factories import WishlistCallback, ItemCallback
from keyboards.inline import GetInlineKeyboardMarkup
from src import strings

router = Router()


@router.callback_query(WishlistCallback.filter(F.action == 'show'))
async def show_wishlist_handler(call: types.CallbackQuery, callback_data: WishlistCallback):
    # await call.message.delete_reply_markup()
    await call.answer(cache_time=5)
    wishlist_id = callback_data.wishlist_id
    wishlist = await WishlistCommand.get(wishlist_id)
    await show_wishlist(call.message, call.from_user.id, wishlist)


async def show_wishlist(message: types.Message, user_id: int, wishlist: Wishlist):
    owner = await UserCommand.get(wishlist.creator_tg_id)
    wishlist_items = await ItemCommand.get_all_wishlist_items(wishlist.id)
    if owner.tg_id == user_id:
        is_owner = True
    else:
        is_owner = False
    markup = GetInlineKeyboardMarkup.list_wishlist_items(
        items=wishlist_items,
        wishlist_id=wishlist.id,
        wishlist_hashcode=wishlist.hashcode,
        is_owner=is_owner
    )

    text = strings.wishlist_title(wishlist, owner) + '\n\n' + strings.items_list
    await message.answer(text, reply_markup=markup)


@router.message(Command('my_wishlists'))
@router.message(F.text == strings.my_wishlists)
async def show_user_wishlists(message: types.Message):
    """
    List all user's wishlists
    """
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
