from aiogram import Router, types, F, Bot
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from bot import strings
from bot.db.queries.gift_ideas import get_all_gift_ideas_categories, get_gift_idea_by_id, add_gift_idea_to_wishlist
from bot.db.queries.users import get_user_or_none_by_telegram_id
from bot.db.queries.wishlists import get_wishlist_by_id
from bot.keyboards.callback_factories import GiftIdeaCallback, AddGiftIdeaToWishlistCallback, GoToGiftIdeasCallback
from bot.keyboards.inline import get_categories_keyboard, get_gift_idea_keyboard, \
    choose_wishlist_to_add_gift_idea_keyboard, wishlist_items_keyboard, go_to_menu_or_add_another_item

main_menu_router = Router()
router = Router()


@main_menu_router.message(F.text == strings.gift_ideas)
@main_menu_router.callback_query(GoToGiftIdeasCallback.filter())
async def gift_ideas_select_category_handler(
        update: types.Message | types.CallbackQuery,
        state: FSMContext,
        session: AsyncSession
):
    await state.clear()

    gift_ideas_categories = await get_all_gift_ideas_categories(session)
    if isinstance(update, types.Message):
        await update.answer(
            strings.gift_ideas_categories,
            reply_markup=get_categories_keyboard(gift_ideas_categories)
        )
    elif isinstance(update, types.CallbackQuery):
        await update.message.answer(
            strings.gift_ideas_categories,
            reply_markup=get_categories_keyboard(gift_ideas_categories)
        )


# @router.callback_query(GiftCategoryCallback.filter())
# async def gift_ideas_handler(
#         call: types.CallbackQuery,
#         callback_data: GiftCategoryCallback,
#         session: AsyncSession,
# ):
#     await call.answer(cache_time=3)
#     category_id = callback_data.category_id
#     category = await get_category_by_id(session, category_id)
#     await call.message.answer(
#         strings.gift_ideas_for_this_category(category.name),
#         reply_markup=get_list_gift_ideas_keyboard(category.gift_ideas)
#     )


# @router.callback_query(GiftIdeaCallback.filter(F.action == "show"))
# async def show_gift_idea_handler(
#         call: types.CallbackQuery,
#         callback_data: GiftIdeaCallback,
#         session: AsyncSession
# ):
#     await call.answer(cache_time=3)
#     gift_idea_id = callback_data.gift_idea_id
#     gift_idea = await get_gift_idea_by_id(session, gift_idea_id)
#     if gift_idea.description:
#         text = f"<b>{gift_idea.title}</b>\n\n{gift_idea.description}"
#     else:
#         text = f"<b>{gift_idea.title}</b>"
#     reply_markup = get_gift_idea_keyboard(gift_idea)
#     if gift_idea.photo_file_id:
#         await call.message.answer_photo(
#             gift_idea.photo_file_id,
#             caption=text,
#             reply_markup=reply_markup
#         )
#     else:
#         await call.message.answer(
#             text,
#             reply_markup=reply_markup
#         )


@router.callback_query(GiftIdeaCallback.filter(F.action == "choose_wishlist_to_add"))
async def choose_wishlist_to_add_gift_idea_handler(
        call: types.CallbackQuery,
        callback_data: GiftIdeaCallback,
        session: AsyncSession,
        bot: Bot,
):
    gift_idea_id = callback_data.gift_idea_id
    user = await get_user_or_none_by_telegram_id(session, call.from_user.id)
    user_wishlists = list(
        filter(
            lambda wishlist: wishlist.creator_id == user.id and wishlist.is_active is True,
            user.wishlists
        )
    )
    if len(user_wishlists) == 0:
        text = strings.firstly_create_wishlist
    else:
        text = strings.choose_wishlist_to_add_gift_idea
    markup = choose_wishlist_to_add_gift_idea_keyboard(gift_idea_id=gift_idea_id, wishlists=user_wishlists)
    await bot.send_message(
        call.from_user.id,
        text,
        reply_markup=markup
    )


@router.callback_query(AddGiftIdeaToWishlistCallback.filter())
async def add_gift_to_wishlist_handler(
        call: types.CallbackQuery,
        callback_data: AddGiftIdeaToWishlistCallback,
        session: AsyncSession,
):
    await call.answer()
    gift_idea_id = callback_data.gift_idea_id
    wishlist_id = callback_data.wishlist_id
    gift_idea = await get_gift_idea_by_id(session, gift_idea_id)
    await add_gift_idea_to_wishlist(session, gift_idea, wishlist_id)
    await call.message.edit_text(
        strings.gift_idea_successfully_added_to_wishlist,
        reply_markup=go_to_menu_or_add_another_item(wishlist_id=wishlist_id)
    )
