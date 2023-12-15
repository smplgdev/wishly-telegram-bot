import asyncio
from datetime import datetime, timedelta

from aiogram import Bot, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, Update, CallbackQuery
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from sqlalchemy.ext.asyncio import AsyncSession

from bot import strings
from bot.db.queries.secret_list import create_secret_list
from bot.db.queries.users import get_user_or_none_by_telegram_id
from bot.db.queries.wishlists import create_wishlist, add_wishlist_to_favourite
from bot.keyboards.aiogram_calendar.schemas import SimpleCalendarCallback
from bot.keyboards.aiogram_calendar.simple_calendar import SimpleCalendar
from bot.keyboards.callback_factories import WishlistActionsCallback
from bot.keyboards.inline import add_items_keyboard
from bot.states.create_secret_list import CreateSecretListStates
from bot.states.create_wishlist import CreateWishlistStates
from bot.utils.scheduled_jobs.message_to_owners_of_wishlists_after_1_day import send_message_to_owner_of_wishlist
from bot.utils.types import ListTypes


router = Router()
main_menu_router = Router()


@main_menu_router.message(Command('new_wishlist'))
@main_menu_router.message(F.text == strings.create_wishlist)
@router.callback_query(WishlistActionsCallback.filter(F.action == 'create_wishlist'))
async def create_wishlist_handler(update: Update, state: FSMContext, bot: Bot):
    await ask_user_about_list_title(
        bot=bot,
        user_id=update.from_user.id,
        list_type=ListTypes.WISHLIST,
        state=state,
    )


@main_menu_router.message(F.text == strings.secret_list_button)
async def create_secret_list_handler(message: Message, state: FSMContext, bot: Bot):
    await ask_user_about_list_title(
        bot=bot,
        user_id=message.from_user.id,
        list_type=ListTypes.SECRET_LIST,
        state=state
    )


async def ask_user_about_list_title(
        bot: Bot,
        user_id: int,
        list_type: ListTypes,
        state: FSMContext,
):
    await state.clear()
    if list_type == ListTypes.WISHLIST:
        text = strings.enter_wishlist_title
        state_to_set = CreateWishlistStates.title
    elif list_type == ListTypes.SECRET_LIST:
        text = strings.enter_secret_list_title
        state_to_set = CreateSecretListStates.title
    else:
        return

    await state.set_state(state_to_set)

    await bot.send_message(
        chat_id=user_id,
        text=text,
    )


@router.message(CreateWishlistStates.title)
@router.message(CreateSecretListStates.title)
async def handle_list_title_and_start_calendar(message: Message, state: FSMContext):
    if len(message.text) > 64:
        await message.reply(strings.wishlist_title_too_long)
        return

    await state.update_data(list_title=message.text)
    await message.answer(
        strings.enter_expire_date,
        reply_markup=await SimpleCalendar().start_calendar()
    )

    current_state = await state.get_state()
    if current_state == CreateWishlistStates.title:
        state_to_set = CreateWishlistStates.expiration_date
    elif current_state == CreateSecretListStates.title:
        state_to_set = CreateSecretListStates.expiration_date
    else:
        return
    await state.set_state(state_to_set)


@router.callback_query(SimpleCalendarCallback.filter(), CreateWishlistStates.expiration_date)
@router.callback_query(SimpleCalendarCallback.filter(), CreateSecretListStates.expiration_date)
async def process_simple_calendar(
        call: CallbackQuery,
        state: FSMContext,
        callback_data: SimpleCalendarCallback,
        bot: Bot,
        session: AsyncSession,
        scheduler: AsyncIOScheduler,
):
    calendar = SimpleCalendar(
        show_alerts=True
    )
    calendar.set_dates_range(datetime.today(), datetime.today() + timedelta(days=365 * 10))
    selected, selected_date = await calendar.process_selection(call, callback_data)
    if selected:
        await call.message.answer(
            f'Вы выбрали {selected_date.strftime("%d.%m.%Y")}',
        )
        await asyncio.sleep(1)
        current_state = await state.get_state()
        if current_state == CreateWishlistStates.expiration_date:
            await finish_wishlist_create(
                state=state,
                session=session,
                scheduler=scheduler,
                bot=bot,
                user_id=call.from_user.id,
                expiration_date=selected_date,
            )
        elif current_state == CreateSecretListStates.expiration_date:
            await call.message.answer(strings.enter_user_limit)
            await state.update_data(expiration_date=selected_date.strftime("%d.%m.%Y"))
            await state.set_state(CreateSecretListStates.max_participants)


async def finish_wishlist_create(
        state: FSMContext,
        session: AsyncSession,
        scheduler: AsyncIOScheduler,
        bot: Bot,
        user_id: int,
        expiration_date: datetime.date,
):
    data = await state.get_data()
    title = data.get("list_title")
    creator = await get_user_or_none_by_telegram_id(session, telegram_id=user_id)
    wishlist = await create_wishlist(
        session,
        creator_id=creator.id,
        title=title,
        expiration_date=expiration_date
    )
    await add_wishlist_to_favourite(session, user=creator, wishlist=wishlist)
    scheduler.add_job(
        send_message_to_owner_of_wishlist,
        DateTrigger(run_date=datetime.now() + timedelta(days=1)),
        args=(wishlist.id,),
        misfire_grace_time=60 * 60
    )
    await bot.send_message(
        chat_id=user_id,
        text=strings.wishlist_successfully_created(wishlist=wishlist),
        disable_web_page_preview=True,
        reply_markup=add_items_keyboard(wishlist_id=wishlist.id)
    )
    await state.clear()


@router.message(CreateSecretListStates.max_participants)
async def handle_max_participants(message: Message, state: FSMContext, session: AsyncSession):
    if not message.text.isdigit():
        await message.reply(strings.cant_parse_int_error)
        return
    max_participants = int(message.text)
    if not(3 <= max_participants <= 100):
        await message.reply(strings.incorrect_int_error)
        return
    data = await state.get_data()
    title = data.get("list_title")
    expiration_date_str = data.get("expiration_date")
    expiration_date = datetime.strptime(expiration_date_str, "%d.%m.%Y").date()
    creator = await get_user_or_none_by_telegram_id(session, message.from_user.id)
    sl = await create_secret_list(
        session=session,
        creator_id=creator.id,
        title=title,
        expiration_date=expiration_date,
        max_participants=max_participants,
    )
    await message.answer(strings.secret_list_successfully_created(sl.title, sl.hashcode))
    await state.clear()
