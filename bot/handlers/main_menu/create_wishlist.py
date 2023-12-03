import datetime

from aiogram import Router, F, types, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from sqlalchemy.ext.asyncio import AsyncSession

from bot import strings
from bot.db.queries.users import get_user_or_none_by_telegram_id
from bot.db.queries.wishlists import create_wishlist, add_wishlist_to_favourite, make_wishlist_inactive
from bot.keyboards.callback_factories import WishlistActionsCallback
from bot.keyboards.inline import add_items_keyboard
from bot.states.create_wishlist import CreateWishlistStates
from bot.utils.scheduled_jobs.message_to_owners_of_wishlists_after_1_day import send_message_to_owner_of_wishlist

router = Router()
main_menu_router = Router()


@main_menu_router.message(Command('new_wishlist'))
@main_menu_router.message(F.text == strings.create_wishlist)
async def create_wishlist_handler(message: types.Message, state: FSMContext):
    await create_wishlist_step1(message, state)


@router.callback_query(WishlistActionsCallback.filter(F.action == 'create_wishlist'))
async def create_wishlist_callback_handler(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    await create_wishlist_step1(call.message, state)


async def create_wishlist_step1(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(strings.enter_wishlist_title)
    await state.set_state(CreateWishlistStates.title)


@router.message(CreateWishlistStates.title)
async def create_wishlist_step2(message: types.Message, state: FSMContext):
    if len(message.text) > 64:
        await message.reply(strings.wishlist_title_too_long)
        return
    await state.update_data(wishlist_title=message.text)
    await message.answer(strings.enter_expire_date)
    await state.set_state(CreateWishlistStates.expiration_date)

    # TODO: Make calendar inline mode


@router.message(CreateWishlistStates.expiration_date)
async def create_wishlist_finish(
        message: types.Message,
        state: FSMContext,
        session: AsyncSession,
        scheduler: AsyncIOScheduler,
        bot: Bot,
):
    try:
        date = datetime.datetime.strptime(message.text, "%d.%m.%Y").date()
    except ValueError:
        await message.reply(strings.date_value_error)
        return
    if date < datetime.date.today():
        await message.reply(strings.past_date_error)
        return
    data = await state.get_data()
    title = data.get("wishlist_title")
    creator = await get_user_or_none_by_telegram_id(session, telegram_id=message.from_user.id)
    wishlist = await create_wishlist(session, creator_id=creator.id,
                                     title=title, expiration_date=date)
    user = await get_user_or_none_by_telegram_id(session, message.from_user.id)
    await add_wishlist_to_favourite(session, user=user, wishlist=wishlist)
    scheduler.add_job(
        send_message_to_owner_of_wishlist,
        DateTrigger(run_date=datetime.datetime.now() + datetime.timedelta(days=1)),
        args=(wishlist.id,),
        misfire_grace_time=60*60
    )
    await message.answer(strings.wishlist_successfully_created(wishlist=wishlist),
                         reply_markup=add_items_keyboard(wishlist_id=wishlist.id))
    await state.clear()
