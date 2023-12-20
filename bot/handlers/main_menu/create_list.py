import asyncio
import html
from datetime import datetime, timedelta, date

from aiogram import Bot, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from sqlalchemy.ext.asyncio import AsyncSession

from bot import strings
from bot.db.queries.users import get_user_or_none_by_telegram_id, update_user
from bot.db.queries.wishlists import create_wishlist, add_wishlist_to_favourite
from bot.keyboards.aiogram_calendar.schemas import SimpleCalendarCallback
from bot.keyboards.aiogram_calendar.simple_calendar import SimpleCalendar
from bot.keyboards.callback_factories import WishlistActionsCallback, WishlistPurposeCallback
from bot.keyboards.inline import add_items_keyboard, wishlist_purposes_keyboard
from bot.states.create_wishlist import CreateWishlistStates
from bot.utils.photo_file_ids import get_picture_file_id
from bot.utils.scheduled_jobs.message_to_owners_of_wishlists_after_1_day import send_message_to_owner_of_wishlist
from bot.utils.send_message import send_message

router = Router()
main_menu_router = Router()


@main_menu_router.message(Command('new_wishlist'))
@main_menu_router.message(F.text == strings.create_wishlist)
@router.callback_query(WishlistActionsCallback.filter(F.action == 'create_wishlist'))
async def create_wishlist_handler(update: Message | CallbackQuery, state: FSMContext, bot: Bot):
    await state.clear()
    text_1 = strings.choose_wishlist_purpose_1
    user_id = update.from_user.id

    photo_file_id = get_picture_file_id("create_wishlist")
    await bot.send_photo(
        chat_id=user_id,
        photo=photo_file_id,
        caption=text_1
    )
    await bot.send_chat_action(user_id, "typing")
    await asyncio.sleep(3)
    text_2 = strings.choose_wishlist_purpose_2
    markup = wishlist_purposes_keyboard()
    await send_message(
        bot=bot,
        user_id=user_id,
        text=text_2,
        reply_markup=markup
    )
    await state.set_state(CreateWishlistStates.purpose)


@router.callback_query(CreateWishlistStates.purpose, WishlistPurposeCallback.filter())
async def get_wishlist_purpose_handler(call: CallbackQuery,
                                       session: AsyncSession,
                                       callback_data: WishlistPurposeCallback,
                                       state: FSMContext,
                                       bot: Bot):
    await call.message.delete_reply_markup()
    wl_purpose = callback_data.purpose
    await state.update_data(wl_purpose=wl_purpose)
    if wl_purpose == strings.BIRTHDAY_PURPOSE:
        await call.message.answer(strings.how_old_are_you_1)
        user = await get_user_or_none_by_telegram_id(session=session, telegram_id=call.from_user.id)
        if user.date_of_birth:
            await state.update_data(user_age=date.today().year - user.date_of_birth.year)
        await bot.send_chat_action(call.from_user.id, "typing")
        await asyncio.sleep(4)
        await call.message.answer(strings.how_old_are_you_2)
        await state.set_state(CreateWishlistStates.user_age)
        return
    await ask_user_about_list_title(
        bot=bot,
        user_id=call.from_user.id,
        state=state,
        wl_purpose=wl_purpose
    )


@router.message(CreateWishlistStates.user_age)
async def get_user_age_handler(message: Message,
                               state: FSMContext,
                               bot: Bot):
    user_age = str()
    for ch in message.text:
        if ch.isdigit():
            user_age += ch
    user_age = int(user_age)
    if not user_age:
        await message.answer(strings.enter_age_error)
        return
    if not(0 <= user_age < 100):
        await message.answer(strings.enter_age_error)
        return
    await state.update_data(user_age=user_age)
    await ask_user_about_list_title(
        bot=bot,
        user_id=message.from_user.id,
        state=state,
        wl_purpose=strings.BIRTHDAY_PURPOSE
    )


async def ask_user_about_list_title(
        bot: Bot,
        user_id: int,
        state: FSMContext,
        wl_purpose: str
):

    await bot.send_photo(
        chat_id=user_id,
        photo=get_picture_file_id("holiday_atmosphere"),
        caption=strings.enter_wishlist_title_1,
    )
    await bot.send_chat_action(user_id, "typing")
    await asyncio.sleep(2.5)
    await bot.send_message(
        chat_id=user_id,
        text=strings.enter_wishlist_title_2(wl_purpose=wl_purpose)
    )
    await state.set_state(CreateWishlistStates.title)


@router.message(CreateWishlistStates.title)
async def handle_list_title_and_start_calendar(
        message: Message,
        state: FSMContext,
        session: AsyncSession,
        scheduler: AsyncIOScheduler,
        bot: Bot,
):
    if len(message.text) > 64:
        await message.reply(strings.wishlist_title_too_long)
        return

    await state.update_data(list_title=html.escape(message.text))
    data = await state.get_data()
    wl_purpose = data.get("wl_purpose")
    if wl_purpose == strings.NEW_YEAR_PURPOSE:
        expiration_date = date(year=date.today().year, month=12, day=31)
        await finish_wishlist_create(
            state=state,
            session=session,
            scheduler=scheduler,
            bot=bot,
            user_id=message.from_user.id,
            expiration_date=expiration_date
        )
        return
    await message.answer(
        strings.enter_expire_date,
        reply_markup=await SimpleCalendar().start_calendar()
    )

    await state.set_state(CreateWishlistStates.expiration_date)


@router.callback_query(SimpleCalendarCallback.filter(), CreateWishlistStates.expiration_date)
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
            f'Выбранный день: {selected_date.strftime("%d.%m.%Y")}'
            f'\n\nПодожди несколько секунд, пока я создаю твой вишлист!',
        )
        await bot.send_chat_action(call.from_user.id, "typing")
        await asyncio.sleep(4)
        await finish_wishlist_create(
            state=state,
            session=session,
            scheduler=scheduler,
            bot=bot,
            user_id=call.from_user.id,
            expiration_date=selected_date,
        )


async def finish_wishlist_create(
        state: FSMContext,
        session: AsyncSession,
        scheduler: AsyncIOScheduler,
        bot: Bot,
        user_id: int,
        expiration_date: date,
):
    data = await state.get_data()
    title = data.get("list_title")
    purpose = data.get("wl_purpose")
    creator = await get_user_or_none_by_telegram_id(session, telegram_id=user_id)

    wishlist = await create_wishlist(
        session,
        creator_id=creator.id,
        title=title,
        purpose=purpose,
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

    if purpose == strings.BIRTHDAY_PURPOSE:
        user_age = data.get("user_age")
        await update_user(session, user=creator,
                          date_of_birth=date(year=expiration_date.year - user_age,
                                             month=expiration_date.month,
                                             day=expiration_date.day))

    await state.clear()
