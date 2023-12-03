import datetime

from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from sqlalchemy.ext.asyncio import AsyncSession

from bot import strings
from bot.db.models.users import User
from bot.db.queries.users import get_user_or_none_by_id
from bot.db.queries.wishlists import get_wishlist_by_hashcode, add_wishlist_to_favourite, delete_wishlist
from bot.keyboards.default import start_keyboard
from bot.keyboards.inline import go_to_wishlist_keyboard
from bot.utils.get_deep_link import get_deep_link
from bot.utils.scheduled_jobs.message_to_deeplinked_users import send_message_to_deeplinked_user

main_menu_router = Router()


@main_menu_router.message(Command('home'))
@main_menu_router.message(CommandStart())
async def cmd_start(
        message: Message,
        state: FSMContext,
        session: AsyncSession,
        user: User,
        scheduler: AsyncIOScheduler,
        ):
    await state.clear()
    deep_link = get_deep_link(message.text)

    await message.answer(
        strings.start_text(message.from_user.first_name),
        reply_markup=start_keyboard()
    )

    if deep_link:
        hashcode = deep_link
        wishlist = await get_wishlist_by_hashcode(session, hashcode)
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
