import datetime
import random

from aiogram import Router, Bot
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from sqlalchemy.ext.asyncio import AsyncSession

from bot import strings
from bot.db.models.users import User
from bot.db.queries.secret_list import get_secret_list_or_none_by_hashcode, add_participant, delete_participant, \
    create_wishlist_for_secret_list_participant, \
    update_participant
from bot.db.queries.users import get_user_or_none_by_id
from bot.db.queries.wishlists import get_wishlist_by_hashcode, add_wishlist_to_favourite
from bot.keyboards.default import start_keyboard
from bot.keyboards.inline import go_to_wishlist_keyboard, go_to_secret_list, add_items_keyboard
from bot.strings import formatted_user_string
from bot.utils.get_deep_link import get_deep_link
from bot.utils.run_secret_list_game import run_secret_list_game
from bot.utils.scheduled_jobs.message_to_deeplinked_users import send_message_to_deeplinked_user
from bot.utils.send_message import send_message
from bot.utils.types import ListTypes

main_menu_router = Router()


@main_menu_router.message(Command('home'))
@main_menu_router.message(CommandStart())
async def cmd_start(
        message: Message,
        state: FSMContext,
        session: AsyncSession,
        user: User,
        scheduler: AsyncIOScheduler,
        bot: Bot
        ):
    await state.clear()
    list_type, hash_code = get_deep_link(message.text)
    await message.answer(
        strings.start_text(message.from_user.first_name),
        reply_markup=start_keyboard()
    )

    if list_type == ListTypes.WISHLIST:
        wishlist = await get_wishlist_by_hashcode(session, hash_code)
        if not wishlist:
            await message.answer(strings.wishlist_not_found)
            return
        creator_user = await get_user_or_none_by_id(session, wishlist.creator_id)

        await message.answer(
            strings.wishlist_found_in_deep_link(
                wishlist=wishlist,
                creator_user=creator_user
            ),
            reply_markup=go_to_wishlist_keyboard(wishlist.id)
        )

        await add_wishlist_to_favourite(session, user, wishlist)
        scheduler.add_job(
            send_message_to_deeplinked_user,
            DateTrigger(run_date=datetime.datetime.now() + datetime.timedelta(hours=4)),
            args=(message.from_user.id, wishlist.id),
            misfire_grace_time=60*60
        )
    else:
        return
    # elif list_type == ListTypes.SECRET_LIST:
    #     secret_list = await get_secret_list_or_none_by_hashcode(session, hashcode=hash_code)
    #     if not secret_list:
    #         await message.answer(strings.secret_list_not_found)
    #         return
    #     elif secret_list.status in ["running", "finished"]:
    #         await message.answer(strings.secret_list_finished)
    #         return
    #     elif user.id in [p.user.id or None for p in secret_list.participants]:
    #         await message.answer(strings.you_already_in_secret_list)
    #         return
    #     elif user.id == secret_list.creator_id:
    #         await message.answer(strings.you_are_admin_of_this_secret_list)
    #         return
    #     participant = await add_participant(session, sl_id=secret_list.id, user_id=user.id)
    #     wishlist = await create_wishlist_for_secret_list_participant(
    #         session,
    #         creator_id=user.id,
    #         participant_id=participant.id,
    #         expiration_date=secret_list.expiration_date,
    #     )
    #     await update_participant(session, participant, wishlist_id=wishlist.id)
    #     await add_wishlist_to_favourite(session, user=user, wishlist=wishlist)
    #     await session.refresh(participant)
    #     await session.refresh(secret_list)
    #     creator_user = await get_user_or_none_by_id(session, secret_list.creator_id)
    #     greeting_phrase = strings.new_user_joined_to_secret_list(joined_user=user,
    #                                                              sl_title=secret_list.title)
    #     deleted_participants_counter = 0
    #     for participant in secret_list.participants:
    #         if participant.user.telegram_id == message.from_user.id:
    #             markup = InlineKeyboardMarkup(
    #                 inline_keyboard=add_items_keyboard(wishlist_id=wishlist.id).inline_keyboard
    #                                 + go_to_secret_list(sl_id=secret_list.id,
    #                                                     participant_id=participant.id).inline_keyboard)
    #         else:
    #             markup = go_to_secret_list(sl_id=secret_list.id, participant_id=participant.id) if random.randint(1, 3) == 1 else None
    #         is_sent = await send_message(
    #             bot=bot,
    #             user_id=participant.user.telegram_id,
    #             text=greeting_phrase,
    #             disable_notification=True,
    #             reply_markup=markup,
    #         )
    #
    #         if is_sent is False:
    #             await delete_participant(session, participant=participant)
    #             await send_message(
    #                 bot=bot,
    #                 user_id=creator_user.telegram_id,
    #                 text=strings.participant_was_deleted % formatted_user_string(participant.user),
    #             )
    #             deleted_participants_counter += 1
    #
    #     # Message for secret list owner
    #     await send_message(
    #         bot=bot,
    #         user_id=creator_user.telegram_id,
    #         text=greeting_phrase,
    #     )
    #
    #     if len(secret_list.participants) - deleted_participants_counter == secret_list.max_participants:
    #         await run_secret_list_game(session, bot, sl_id=secret_list.id)
