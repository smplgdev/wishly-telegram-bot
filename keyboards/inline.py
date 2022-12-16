from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.models.Item import Item
from database.models.Wishlist import Wishlist
from keyboards.callback_factories import WishlistCallback, ItemCallback
from src import strings


class GetInlineKeyboardMarkup:
    @staticmethod
    def add_items(wishlist_id: int) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.button(text=strings.add_item_to_wishlist, callback_data=WishlistCallback(wishlist_id=wishlist_id,
                                                                                         action="add"))
        return builder.as_markup()

    @staticmethod
    def skip(wishlist_id: int, stage: str):
        builder = InlineKeyboardBuilder()
        builder.button(text=strings.skip_stage, callback_data=WishlistCallback(wishlist_id=wishlist_id,
                                                                               action="skip",
                                                                               stage=stage))
        return builder.as_markup()

    @staticmethod
    def apply_or_discard_adding_to_wishlist(wishlist_id: int):
        builder = InlineKeyboardBuilder()
        builder.button(text=strings.apply_adding_to_wishlist, callback_data=WishlistCallback(wishlist_id=wishlist_id,
                                                                                             action="apply_adding"))
        builder.button(text=strings.discard_adding_to_wishlist, callback_data=WishlistCallback(wishlist_id=wishlist_id,
                                                                                               action="discard_adding"))
        return builder.as_markup()

    @staticmethod
    def main_menu_or_another_item(wishlist_id: int):
        builder = InlineKeyboardBuilder()
        builder.button(text=strings.add_one_more_item,
                       callback_data=WishlistCallback(wishlist_id=wishlist_id,
                                                      action="add_another_item"))
        builder.button(text=strings.go_to_wishlist,
                       callback_data=WishlistCallback(wishlist_id=wishlist_id,
                                                      action="show"))
        builder.button(text=strings.main_menu, callback_data=WishlistCallback(wishlist_id=wishlist_id,
                                                                              action="main_menu"))
        builder.adjust(1)
        return builder.as_markup()

    @staticmethod
    def go_to_wishlist(wishlist_id: int):
        builder = InlineKeyboardBuilder()
        builder.button(text=strings.go_to_friend_wishlist,
                       callback_data=WishlistCallback(wishlist_id=wishlist_id,
                                                      action="show"))
        return builder.as_markup()

    @staticmethod
    def list_user_wishlists(wishlists: list[Wishlist]):
        builder = InlineKeyboardBuilder()
        for wishlist in wishlists:
            if not wishlist.is_active:
                continue
            builder.button(
                text=f"{wishlist.title[:32]} ({wishlist.expiration_date.strftime('%d.%m.%Y')})",
                callback_data=WishlistCallback(wishlist_id=wishlist.id,
                                               action="show")
            )
        builder.button(
            text=strings.create_wishlist_inline_button,
            callback_data=WishlistCallback(
                wishlist_id=0,
                action="create_wishlist"
            )
        )
        builder.adjust(1)
        return builder.as_markup()

    @staticmethod
    def list_related_wishlists(wishlists: list[Wishlist]):
        builder = InlineKeyboardBuilder()
        for wishlist in wishlists:
            builder.button(
                text=f"{wishlist.title[:32]} ({wishlist.expiration_date.strftime('%d.%m.%Y')})",
                callback_data=WishlistCallback(wishlist_id=wishlist.id,
                                               action="show")
            )
        builder.button(
            text=strings.find_wishlist,
            callback_data=WishlistCallback(
                wishlist_id=0,
                action="find_wishlist"
            )
        )
        builder.adjust(1)
        return builder.as_markup()

    @staticmethod
    def list_wishlist_items(
            wishlist_id: int,
            wishlist_hashcode: str,
            show_hide_wishlist_button: bool = False,
            is_owner: bool = False,
    ) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()

        builder.button(text=strings.show_items_list,
                       switch_inline_query_current_chat=wishlist_hashcode)

        builder.button(text=strings.share_wishlist,
                       switch_inline_query=f"wl_{wishlist_hashcode}")

        if show_hide_wishlist_button:
            builder.button(text=strings.hide_wishlist,
                           callback_data=WishlistCallback(wishlist_id=wishlist_id,
                                                          action="hide"))

        if is_owner:
            builder.button(text=strings.add_item_to_wishlist,
                           callback_data=WishlistCallback(wishlist_id=wishlist_id,
                                                          action="add"))
            builder.button(text=strings.delete_wishlist,
                           callback_data=WishlistCallback(wishlist_id=wishlist_id,
                                                          action="delete_wishlist"))
            # builder.button(text=strings.edit_wishlist,
            #                callback_data=WishlistCallback(wishlist_id=wishlist_id,
            #                                               action="edit"))
        builder.adjust(1)
        return builder.as_markup()

    @staticmethod
    def item_markup(
            item: Item,
            wishlist_hashcode: str,
            is_owner: bool = False
    ):
        builder = InlineKeyboardBuilder()
        if item.buyer_tg_id is None:
            builder.button(text=strings.i_will_gift_this_item,
                           callback_data=ItemCallback(wishlist_id=item.wishlist_id,
                                                      item_id=item.id,
                                                      action="gift")
                           )
        else:
            builder.button(text=strings.someone_else_gift_it,
                           callback_data="null")
        if is_owner:
            builder.button(text=strings.delete_item,
                           callback_data=ItemCallback(wishlist_id=item.wishlist_id,
                                                      item_id=item.id,
                                                      action="delete"))
        builder.button(text=strings.show_items_list,
                       switch_inline_query_current_chat=wishlist_hashcode)
        builder.adjust(1)
        return builder.as_markup()

    @staticmethod
    def edit_or_delete_wishlist(wishlist_id: int):
        builder = InlineKeyboardBuilder()
        builder.button(text=strings.add_item_to_wishlist,
                       callback_data=WishlistCallback(wishlist_id=wishlist_id,
                                                      action="add"))
        builder.button(text=strings.delete_wishlist,
                       callback_data=WishlistCallback(wishlist_id=wishlist_id,
                                                      action="delete_wishlist"))
        builder.adjust(1)
        return builder.as_markup()

    @staticmethod
    def delete_wishlist_or_not(wishlist_id: int):
        builder = InlineKeyboardBuilder()
        builder.button(text=strings.yes_delete,
                       callback_data=WishlistCallback(wishlist_id=wishlist_id,
                                                      action="yes_delete"))
        builder.button(text=strings.no_delete,
                       callback_data=WishlistCallback(wishlist_id=wishlist_id,
                                                      action="no_delete"))
        builder.adjust(2)
        return builder.as_markup()
