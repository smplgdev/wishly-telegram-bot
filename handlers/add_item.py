from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from bot import bot
from database.pgcommands.commands import ItemCommand
from keyboards.callback_factories import WishlistCallback
from keyboards.default import GetKeyboardMarkup
from keyboards.inline import GetInlineKeyboardMarkup
from src import strings
from states.item import AddItem

router = Router()


@router.callback_query(WishlistCallback.filter(F.action.in_(["add", "add_another_item"])))
async def add_new_item_to_wishlist(call: types.CallbackQuery, state: FSMContext, callback_data: WishlistCallback):
    await call.message.answer(strings.enter_item_title)
    await state.update_data(wishlist_id=callback_data.wishlist_id)
    await state.set_state(AddItem.title)
    await call.answer(cache_time=10)


@router.message(AddItem.title)
async def add_new_item_to_wishlist_step2(message: types.Message, state: FSMContext):
    title = message.text
    if len(title) > 64:
        await message.reply(strings.item_title_too_long)
        return
    await state.update_data(item_title=title)
    await message.answer(strings.item_description,
                         reply_markup=GetKeyboardMarkup.skip())
    await state.set_state(AddItem.description)


@router.message(AddItem.description, F.content_type == 'text')
async def add_new_item_to_wishlist_step3(message: types.Message, state: FSMContext):
    description = message.text
    if len(description) > 256:
        await message.reply(strings.item_description_too_long)
        return
    if description != strings.skip_stage:
        await state.update_data(item_description=description)
    await message.answer(strings.attach_item_photo,
                         reply_markup=GetKeyboardMarkup.skip())
    await state.set_state(AddItem.photo)


@router.message(AddItem.photo, F.content_type.in_(['photo', 'text']))
async def add_new_item_to_wishlist_step4(message: types.Message, state: FSMContext):
    photo_file_id = None
    if message.text != strings.skip_stage and message.photo:
        photo_file_id = message.photo[-1].file_id
        await state.update_data(item_photo_file_id=photo_file_id)
    data = await state.get_data()
    title = data.get("item_title")
    description = data.get("item_description")
    item_text = strings.item_info_text(title, description)
    if photo_file_id is None:
        msg = await message.answer(item_text, reply_markup=ReplyKeyboardRemove())
    else:
        msg = await message.answer_photo(photo=photo_file_id,
                                         caption=item_text,
                                         reply_markup=ReplyKeyboardRemove())
    wishlist_id = int(data.get("wishlist_id"))
    markup = GetInlineKeyboardMarkup.apply_or_discard_adding_to_wishlist(wishlist_id)
    await bot.send_message(message.from_user.id,
                           strings.reply_item_info_example,
                           reply_to_message_id=msg.message_id,
                           reply_markup=markup)
    await state.set_state(AddItem.final)


@router.callback_query(AddItem.final, WishlistCallback.filter(F.action == "apply_adding"))
async def apply_adding_item_handler(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    wishlist_id = data.get("wishlist_id")
    title = data.get("item_title")
    description = data.get("item_description")
    photo_file_id = data.get("item_photo_file_id")
    await ItemCommand.add(wishlist_id=wishlist_id,
                          title=title,
                          description=description,
                          photo_file_id=photo_file_id)
    markup = GetInlineKeyboardMarkup.main_menu_or_another_item(wishlist_id=wishlist_id)
    await call.message.edit_text(strings.creating_item_apply, reply_markup=markup)
    await state.clear()


@router.callback_query(AddItem.final, WishlistCallback.filter(F.action == "discard_adding"))
async def discard_adding_item_handler(call: types.CallbackQuery, state: FSMContext, callback_data: WishlistCallback):
    wishlist_id = callback_data.wishlist_id
    await state.clear()
    markup = GetInlineKeyboardMarkup.main_menu_or_another_item(wishlist_id=wishlist_id)
    await call.message.edit_text(strings.creating_item_discard, reply_markup=markup)
