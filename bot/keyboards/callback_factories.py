from typing import Optional

from aiogram.filters.callback_data import CallbackData


class WishlistActionsCallback(CallbackData, prefix="wishlist"):
    wishlist_id: int
    action: str


class ItemActionsCallback(CallbackData, prefix="addItemActions"):
    wishlist_id: int
    action: str


class GiftItemCallback(CallbackData, prefix="giftItem"):
    item_id: int


class AddItemSkipStageCallback(CallbackData, prefix="skipStage"):
    wishlist_id: int
    stage: str


class ItemCallback(CallbackData, prefix="item"):
    wishlist_id: int
    item_id: int
    action: str


class MainMenuCallback(CallbackData, prefix='main_menu'):
    pass


class DeleteItemCallback(CallbackData, prefix="delete_item"):
    item_id: int


class GiftCategoryCallback(CallbackData, prefix="gift_category"):
    category_id: int


class GiftIdeaCallback(CallbackData, prefix="gift_idea"):
    gift_idea_id: int
    action: str


class AddGiftIdeaToWishlistCallback(CallbackData, prefix="add_gift_idea"):
    gift_idea_id: int
    wishlist_id: int


class WishlistToGiftIdeaCallback(CallbackData, prefix="admin"):
    wishlist_id: int
