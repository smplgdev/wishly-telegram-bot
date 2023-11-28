from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.db.models import Item
from bot.db.models import Wishlist
from bot.db.models.gift_ideas import GiftIdea
from bot.db.models.gift_ideas_categories import GiftIdeaCategory
from bot.keyboards.callback_factories import WishlistActionsCallback, ItemActionsCallback, \
    MainMenuCallback, AddItemSkipStageCallback, GiftItemCallback, DeleteItemCallback, GiftCategoryCallback, \
    GiftIdeaCallback, AddGiftIdeaToWishlistCallback
from bot import strings


def go_to_wishlist_keyboard(wishlist_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=strings.go_to_friend_wishlist,
        callback_data=WishlistActionsCallback(
            wishlist_id=wishlist_id,
            action="show_wishlist"
        )
    )
    return builder.as_markup()


def add_items_keyboard(wishlist_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=strings.add_item_to_wishlist,
        callback_data=ItemActionsCallback(
            wishlist_id=wishlist_id,
            action="new_item",
        )
    )
    return builder.as_markup()


def skip_stage_inline_button(wishlist_id: int, stage: str):
    builder = InlineKeyboardBuilder()
    builder.button(
        text=strings.skip_stage,
        callback_data=AddItemSkipStageCallback(
            wishlist_id=wishlist_id,
            stage=stage
        )
    )
    return builder.as_markup()


def ask_user_for_adding_item(wishlist_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(
        text=strings.apply_adding_to_wishlist,
        callback_data=ItemActionsCallback(
            wishlist_id=wishlist_id,
            action="apply_add_item",
        )
    )
    builder.button(
        text=strings.discard_adding_to_wishlist,
        callback_data=ItemActionsCallback(
            wishlist_id=wishlist_id,
            action="discard_add_item",
        )
    )
    return builder.as_markup()


def go_to_menu_or_add_another_item(wishlist_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(
        text=strings.add_one_more_item,
        callback_data=ItemActionsCallback(
            wishlist_id=wishlist_id,
            action="new_item",
        )
    )
    builder.button(
        text=strings.go_to_wishlist,
        callback_data=WishlistActionsCallback(
            wishlist_id=wishlist_id,
            action="show_wishlist",
        )
    )
    builder.button(
        text=strings.main_menu,
        callback_data=MainMenuCallback()
    )
    builder.adjust(1)
    return builder.as_markup()


def add_items(wishlist_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=strings.add_item_to_wishlist,
        callback_data=WishlistActionsCallback(
            wishlist_id=wishlist_id,
            action="add"
        )
    )
    return builder.as_markup()


def apply_or_discard_adding_item_to_wishlist(wishlist_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(
        text=strings.apply_adding_to_wishlist,
        callback_data=WishlistActionsCallback(
            wishlist_id=wishlist_id,
            action="apply_adding"
        )
    )
    builder.button(
        text=strings.discard_adding_to_wishlist,
        callback_data=WishlistActionsCallback(
            wishlist_id=wishlist_id,
            action="discard_adding"
        )
    )
    return builder.as_markup()


def go_back_to_wishlist(wishlist_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(
        text=strings.go_back_without_changes,
        callback_data=WishlistActionsCallback(
            wishlist_id=wishlist_id,
            action="show_wishlist"
        )
    )
    return builder.as_markup()


def list_user_wishlists(wishlists: list[Wishlist], user_id: int):
    builder = InlineKeyboardBuilder()
    for wishlist in wishlists:
        if wishlist.creator_id == user_id:
            creator_prefix = "💎 "
        else:
            creator_prefix = ""
        if len(wishlist.title) > 28:
            wishlist_title = wishlist.title[:28] + '...'
        else:
            wishlist_title = wishlist.title
        builder.button(
            text=f"{creator_prefix}{wishlist_title} ({wishlist.expiration_date.strftime('%d.%m.%y')})",
            callback_data=WishlistActionsCallback(
                wishlist_id=wishlist.id,
                action="show_wishlist"
            )
        )
    builder.button(
        text=strings.create_wishlist_inline_button,
        callback_data=WishlistActionsCallback(
            wishlist_id=0,
            action="create_wishlist"
        )
    )
    builder.adjust(1)
    return builder.as_markup()


def wishlist_items_keyboard(
        wishlist_id: int,
        wishlist_hashcode: str,
        is_owner: bool = False,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text=strings.show_items_list,
        switch_inline_query_current_chat=wishlist_hashcode
    )

    if is_owner:
        builder.button(
            text=strings.add_item_to_wishlist,
            callback_data=ItemActionsCallback(
                wishlist_id=wishlist_id,
                action="new_item",
            )
        )
        builder.button(
            text=strings.edit_wishlist_button_text,
            callback_data=WishlistActionsCallback(
                wishlist_id=wishlist_id,
                action="edit"
            )
        )

    builder.adjust(1)
    return builder.as_markup()


def item_markup(
        item: Item,
        wishlist_hashcode: str,
        is_owner: bool = False
):
    builder = InlineKeyboardBuilder()

    if is_owner:
        if not item.customer_id:
            builder.button(
                text=strings.delete_item,
                callback_data=DeleteItemCallback(
                    item_id=item.id,
                )
            )
    else:
        if item.customer_id is None:
            builder.button(
                text=strings.i_will_gift_this_item,
                callback_data=GiftItemCallback(
                    item_id=item.id,
                )
            )
        else:
            builder.button(
                text=strings.someone_else_gift_it,
                callback_data="null"
            )
    builder.button(
        text=strings.show_items_list,
        switch_inline_query_current_chat=wishlist_hashcode
    )
    builder.adjust(1)
    return builder.as_markup()


def edit_or_delete_wishlist(wishlist_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(
        text=strings.change_title_button_text,
        callback_data=WishlistActionsCallback(
            wishlist_id=wishlist_id,
            action="change_title"
        )
    )
    builder.button(
        text=strings.change_date_button_text,
        callback_data=WishlistActionsCallback(
            wishlist_id=wishlist_id,
            action="change_date"
        )
    )
    builder.button(
        text=strings.delete_wishlist,
        callback_data=WishlistActionsCallback(
            wishlist_id=wishlist_id,
            action="delete_wishlist"
        )
    )
    builder.adjust(1)
    return builder.as_markup()


def delete_wishlist_keyboard(wishlist_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(
        text=strings.yes_delete,
        callback_data=WishlistActionsCallback(
            wishlist_id=wishlist_id,
            action="confirm_deleting_wishlist"
        )
    )
    builder.button(
        text=strings.no_delete,
        callback_data=WishlistActionsCallback(
            wishlist_id=wishlist_id,
            action="discard_deleting_wishlist"
        )
    )
    builder.adjust(2)
    return builder.as_markup()


def get_categories_keyboard(gift_categories):
    builder = InlineKeyboardBuilder()

    for category in gift_categories:
        builder.button(
            text=category.name,
            callback_data=GiftCategoryCallback(
                category_id=category.id
            )
        )

    builder.adjust(2)
    return builder.as_markup()


def get_list_gift_ideas_keyboard(gift_ideas: list[GiftIdea]):
    builder = InlineKeyboardBuilder()

    for gift in gift_ideas:
        builder.button(
            text=gift.title,
            callback_data=GiftIdeaCallback(
                gift_idea_id=gift.id,
                action="show"
            )
        )

    builder.adjust(1)
    return builder.as_markup()


def get_gift_idea_keyboard(gift_idea: GiftIdea):
    builder = InlineKeyboardBuilder()
    builder.button(
        text=strings.add_to_my_wishlist,
        callback_data=GiftIdeaCallback(
            gift_idea_id=gift_idea.id,
            action="choose_wishlist_to_add"
        )
    )
    builder.button(
        text=strings.go_back,
        callback_data=GiftCategoryCallback(
            category_id=gift_idea.gift_idea_category_id
        )
    )
    builder.adjust(1)
    return builder.as_markup()


def choose_wishlist_to_add_gift_idea_keyboard(gift_idea_id: int, wishlists=None):
    builder = InlineKeyboardBuilder()

    for wishlist in wishlists:
        builder.button(
            text=wishlist.title,
            callback_data=AddGiftIdeaToWishlistCallback(
                gift_idea_id=gift_idea_id,
                wishlist_id=wishlist.id
            )
        )
    if not wishlists:
        builder.button(
            text=strings.create_wishlist_inline_button,
            callback_data=WishlistActionsCallback(
                wishlist_id=0,
                action="create_wishlist"
            )
        )
    builder.adjust(1)
    return builder.as_markup()
