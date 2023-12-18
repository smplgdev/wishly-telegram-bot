import io

from aiogram import Router, F, types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession

from bot import strings
from bot.db.queries.items import count_items_in_wishlist, add_item_to_wishlist
from bot.db.queries.secret_list import get_secret_list_or_none_by_id, add_item_to_secret_list, \
    get_participant_or_none_by_id
from bot.db.queries.wishlists import get_wishlist_by_id
from bot.keyboards.callback_factories import ItemActionsCallback, SecretListCallback
from bot.keyboards.default import skip_stage_keyboard
from bot.keyboards.inline import ask_user_for_adding_item, go_to_menu_or_add_another_item, add_gift_to_secret_list
from bot.states.add_item import AddItemStates
from bot.utils.photo_link_telegraph import upload_photo
from bot.utils.types import ListTypes

router = Router()


# @router.callback_query(SecretListCallback.filter(F.action == "add_item"))
# async def add_new_item_to_secret_list(call: types.CallbackQuery,
#                                       state: FSMContext,
#                                       callback_data: SecretListCallback,
#                                       session: AsyncSession):
#     sl_id = callback_data.sl_id
#     sl = await get_secret_list_or_none_by_id(session, sl_id)
#     participant_id = callback_data.participant_id
#     participant = await get_participant_or_none_by_id(session, participant_id)
#     if len(participant.wishlist) == sl.max_gifts:
#         await call.answer(strings.max_gifts_limit_reached % sl.max_gifts, show_alert=True)
#         return
#     await call.message.answer(strings.enter_item_title)
#     await state.update_data(sl_id=sl_id)
#     await state.set_state(AddItemStates.title)
#     await call.answer(cache_time=10)


@router.callback_query(ItemActionsCallback.filter(F.action == "new_item"))
async def add_new_item_to_wishlist(call: types.CallbackQuery, state: FSMContext,
                                   callback_data: ItemActionsCallback, session: AsyncSession):
    wishlist_id = callback_data.wishlist_id
    wishlist = await get_wishlist_by_id(session, wishlist_id)

    item_counter = await count_items_in_wishlist(session, wishlist_id)
    if item_counter > 50 or (wishlist.participant_id and len(wishlist.items) >= 3):
        await call.message.answer(strings.gift_limit_reached)
        return
    await call.message.answer(strings.enter_item_title)
    await state.update_data(wishlist_id=wishlist_id)
    await state.set_state(AddItemStates.title)
    await call.answer(cache_time=10)


@router.message(AddItemStates.title)
async def add_new_item_to_wishlist_step2(message: types.Message, state: FSMContext):
    title = message.text
    if len(title) > 64:
        await message.reply(strings.item_title_too_long)
        return
    await state.update_data(item_title=title)
    await message.answer(
        strings.item_description,
        reply_markup=skip_stage_keyboard()
    )
    await state.set_state(AddItemStates.description)


@router.message(AddItemStates.description, F.content_type == 'text')
async def add_new_item_to_wishlist_step3(message: types.Message, state: FSMContext):
    description = message.text
    if len(description) > 256:
        await message.reply(strings.item_description_too_long)
        return
    if description != strings.skip_stage:
        await state.update_data(item_description=description)
    await message.answer(
        strings.attach_item_photo,
        reply_markup=skip_stage_keyboard()
    )
    await state.set_state(AddItemStates.photo)


@router.message(AddItemStates.photo, F.content_type.in_(['photo', 'text']))
async def add_new_item_to_wishlist_step4(message: types.Message, state: FSMContext, bot: Bot):
    photo_file_id = None
    if message.text != strings.skip_stage and message.photo:
        photo_file_id = message.photo[-1].file_id

        photo_bytes = io.BytesIO()
        await bot.download(message.photo[-1], photo_bytes)
        photo_link = await upload_photo(photo_bytes)

        thumb_bytes = io.BytesIO()
        await bot.download(message.photo[0], thumb_bytes)
        thumb_link = await upload_photo(thumb_bytes)

        await state.update_data(item_photo_file_id=photo_file_id)
        await state.update_data(thumb_link=thumb_link)
        await state.update_data(item_photo_link=photo_link)
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
    wishlist_id = data.get("wishlist_id")
    await bot.send_message(message.from_user.id,
                           strings.reply_item_info_example,
                           reply_to_message_id=msg.message_id,
                           reply_markup=ask_user_for_adding_item(int(wishlist_id)))
    await state.set_state(AddItemStates.final)


@router.callback_query(AddItemStates.final, ItemActionsCallback.filter(F.action == "apply_add_item"))
async def apply_adding_item_handler(call: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    title = data.get("item_title")
    description = data.get("item_description")
    photo_link = data.get("item_photo_link")
    thumb_link = data.get("thumb_link")
    photo_file_id = data.get("item_photo_file_id")
    # if sl_id := data.get("sl_id"):
    #     sl = await get_secret_list_or_none_by_id(session, int(sl_id))
    #     participant = list(filter(lambda p: p.user.telegram_id == call.from_user.id, sl.participants))[0]
    #     await add_item_to_secret_list(
    #         session=session,
    #         participant_id=participant.id,
    #         title=title,
    #         photo_link=photo_link,
    #         thumb_link=thumb_link,
    #         description=description,
    #         photo_file_id=photo_file_id
    #     )
    #     markup = add_gift_to_secret_list(sl_id=int(sl_id), participant_id=participant.id)
    wishlist_id = data.get("wishlist_id")
    await add_item_to_wishlist(
        session=session,
        wishlist_id=int(wishlist_id),
        title=title,
        photo_link=photo_link,
        thumb_link=thumb_link,
        description=description,
        photo_file_id=photo_file_id
    )
    markup = go_to_menu_or_add_another_item(wishlist_id=wishlist_id)

    await call.message.edit_text(strings.creating_item_apply, reply_markup=markup)
    await state.clear()


@router.callback_query(AddItemStates.final, ItemActionsCallback.filter(F.action == "discard_add_item"))
# @router.callback_query(AddItemStates.final, SecretListCallback.filter(F.action == "discard_add_item"))
async def discard_adding_item_handler(call: types.CallbackQuery,
                                      state: FSMContext,
                                      callback_data: SecretListCallback | ItemActionsCallback):
    if isinstance(callback_data, SecretListCallback):
        sl_id = int(callback_data.sl_id)
        participant_id = callback_data.participant_id
        markup = add_gift_to_secret_list(sl_id=sl_id, participant_id=participant_id)
    elif isinstance(callback_data, ItemActionsCallback):
        wishlist_id = int(callback_data.wishlist_id)
        markup = go_to_menu_or_add_another_item(wishlist_id=wishlist_id)
    else:
        return
    await call.message.edit_text(strings.creating_item_discard, reply_markup=markup)
    await state.clear()
