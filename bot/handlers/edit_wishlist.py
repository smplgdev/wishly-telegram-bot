import asyncio
import datetime

from aiogram import Router, F, types, Bot
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from bot import strings
from bot.db.queries.wishlists import get_wishlist_by_id, update_wishlist
from bot.handlers.show_wishlist import show_wishlist
from bot.keyboards.callback_factories import WishlistActionsCallback
from bot.keyboards.inline import edit_or_delete_wishlist, go_back_to_wishlist, delete_wishlist_keyboard
from bot.states.create_wishlist import EditWishlistSettingsStates

router = Router()


@router.callback_query(WishlistActionsCallback.filter(F.action == 'edit'))
async def edit_wishlist_handler(call: types.CallbackQuery,
                                callback_data: WishlistActionsCallback):
    await call.answer(cache_time=20)
    wishlist_id = callback_data.wishlist_id
    markup = edit_or_delete_wishlist(wishlist_id)
    await call.message.answer(
        text=strings.what_you_want_to_do_with_wishlist,
        reply_markup=markup
    )


@router.callback_query(WishlistActionsCallback.filter(F.action == 'change_date'))
async def change_date_handler_step1(
        call: types.CallbackQuery,
        state: FSMContext,
        session: AsyncSession,
        callback_data: WishlistActionsCallback
):
    await call.answer(cache_time=20)
    wishlist_id = callback_data.wishlist_id
    wishlist = await get_wishlist_by_id(session, wishlist_id)
    markup = go_back_to_wishlist(wishlist_id)
    await state.update_data(wishlist_id=wishlist_id)
    await state.set_state(EditWishlistSettingsStates.change_date)
    await call.message.edit_text(
        text=strings.enter_new_expire_date(current_date=wishlist.expiration_date),
        reply_markup=markup
    )


@router.message(EditWishlistSettingsStates.change_date, F.content_type == 'text')
async def change_date_handler_step2(
        message: types.Message,
        state: FSMContext,
        session: AsyncSession,
        bot: Bot,
):
    try:
        date = datetime.datetime.strptime(message.text, "%d.%m.%Y").date()
    except ValueError:
        await message.reply(strings.date_value_error)
        return
    if date < datetime.datetime.today().date():
        await message.reply(strings.past_date_error)
        return
    data = await state.get_data()
    wishlist_id = data.get("wishlist_id")
    wishlist = await get_wishlist_by_id(session, wishlist_id)
    wishlist = await update_wishlist(
        session,
        wishlist=wishlist,
        expiration_date=date
    )
    await message.answer(strings.date_successfully_changed)
    await asyncio.sleep(1)
    await show_wishlist(
        session=session,
        bot=bot,
        user_telegram_id=message.from_user.id,
        wishlist=wishlist
    )


@router.callback_query(WishlistActionsCallback.filter(F.action == 'change_title'))
async def change_title_handler_step1(
        call: types.CallbackQuery,
        state: FSMContext,
        callback_data: WishlistActionsCallback
):
    await call.answer(cache_time=20)
    wishlist_id = callback_data.wishlist_id
    await state.update_data(wishlist_id=wishlist_id)
    await state.set_state(EditWishlistSettingsStates.change_name)
    await call.message.edit_text(
        text=strings.write_new_title,
        reply_markup=go_back_to_wishlist(wishlist_id)
    )


@router.message(EditWishlistSettingsStates.change_name, F.content_type == 'text')
async def change_title_handler_step2(
        message: types.Message,
        state: FSMContext,
        session: AsyncSession,
        bot: Bot,
):
    data = await state.get_data()
    new_title = message.text
    if len(new_title) > 64:
        await message.reply(strings.wishlist_title_too_long)
        return
    wishlist_id = data.get("wishlist_id")
    wishlist = await get_wishlist_by_id(session, wishlist_id)
    wishlist = await update_wishlist(
        session=session,
        wishlist=wishlist,
        title=new_title
    )
    await message.answer(strings.title_successfully_changed)
    await asyncio.sleep(1)
    await show_wishlist(
        session=session,
        bot=bot,
        user_telegram_id=message.from_user.id,
        wishlist=wishlist
    )


@router.callback_query(WishlistActionsCallback.filter(F.action == 'delete_wishlist'))
async def delete_wishlist_handler(call: types.CallbackQuery, callback_data: WishlistActionsCallback):
    wishlist_id = callback_data.wishlist_id
    await call.message.edit_text(
        strings.are_you_sure_to_delete_wishlist,
        reply_markup=delete_wishlist_keyboard(wishlist_id)
    )


@router.callback_query(WishlistActionsCallback.filter(F.action == 'discard_deleting_wishlist'))
async def no_delete_handler(call: types.CallbackQuery):
    await call.answer(strings.delete_cancel, show_alert=True)
    await call.message.delete()


@router.callback_query(WishlistActionsCallback.filter(F.action == 'confirm_deleting_wishlist'))
async def no_delete_handler(
        call: types.CallbackQuery,
        session: AsyncSession,
        callback_data: WishlistActionsCallback
):
    wishlist_id = callback_data.wishlist_id
    wishlist = await get_wishlist_by_id(session, wishlist_id)
    await update_wishlist(session, wishlist, is_active=False)
    await call.answer(strings.delete_successful, show_alert=True)
    await call.message.delete()
