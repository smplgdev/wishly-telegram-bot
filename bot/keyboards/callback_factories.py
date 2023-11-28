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
