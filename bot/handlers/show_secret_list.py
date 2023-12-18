from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot import strings
from bot.db.queries.secret_list import get_secret_list_or_none_by_id
from bot.db.queries.users import get_user_or_none_by_id
from bot.keyboards.callback_factories import SecretListCallback
from bot.keyboards.inline import secret_list_owner_keyboard, add_items_keyboard, wishlist_items_keyboard
from bot.utils.run_secret_list_game import run_secret_list_game

router = Router()


@router.callback_query(SecretListCallback.filter(F.action == "show"))
async def show_secret_list_handler(
        call: CallbackQuery,
        callback_data: SecretListCallback,
        session: AsyncSession
):
    sl = await get_secret_list_or_none_by_id(session, callback_data.sl_id)
    sl_owner = await get_user_or_none_by_id(session, sl.creator_id)
    if sl.status == "waiting":
        if call.from_user.id == sl_owner.telegram_id:
            # Text & keyboard for creator of the secret list
            text = strings.secret_list_owner_text(sl=sl, sl_owner=sl_owner, is_owner=True)
            reply_markup = secret_list_owner_keyboard(sl.id)
        else:
            # Text & keyboard for other users
            participant = list(filter(lambda p: p.user.telegram_id == call.from_user.id, sl.participants))[0]
            text = strings.secret_list_owner_text(sl=sl, sl_owner=sl_owner, is_owner=False)
            reply_markup = add_items_keyboard(wishlist_id=participant.wishlist.id)
    elif sl.status == "running":
        if call.from_user.id == sl_owner.telegram_id:
            # Text & keyboard for creator of the secret list
            text = strings.running_secret_list_owner_text(sl=sl)
            reply_markup = None
        else:
            # Text & keyboard for other users
            participant = list(filter(lambda p: p.user.telegram_id == call.from_user.id, sl.participants))[0]
            giver_wishlist = participant.giver_participant.wishlist
            user_has_gifts: bool = len(giver_wishlist.items) > 0
            text = strings.running_secret_list_participant_text(sl_title=sl.title,
                                                                participants_count=len(sl.participants),
                                                                participant=participant,
                                                                user_has_gifts=user_has_gifts)
            if user_has_gifts:
                reply_markup = wishlist_items_keyboard(wishlist_id=participant.giver_participant.wishlist.id,
                                                       wishlist_hashcode=participant.giver_participant.wishlist.hashcode,
                                                       is_owner=False,
                                                       is_admin=False,
                                                       user_has_gifts=False)
            else:
                reply_markup = None
    else:
        # If event is finished
        if call.from_user.id == sl_owner.telegram_id:
            # Text & keyboard for creator of the secret list
            text = ...
            reply_markup = ...
        else:
            # Text & keyboard for other users
            text = ...
            reply_markup = ...

    await call.message.answer(text=text, reply_markup=reply_markup)
    await call.answer()


@router.callback_query(SecretListCallback.filter(F.action == 'start'))
async def start_game_manually(
        call: CallbackQuery,
        session: AsyncSession,
        callback_data: SecretListCallback,
        bot: Bot,
):
    sl_id = callback_data.sl_id

    sl = await get_secret_list_or_none_by_id(session, sl_id=sl_id)
    if sl.status != "waiting":
        await call.message.answer(strings.game_has_already_started)
        return

    await run_secret_list_game(session, bot=bot, sl_id=sl.id)
