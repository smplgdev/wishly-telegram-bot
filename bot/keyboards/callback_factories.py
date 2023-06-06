from typing import Optional

from aiogram.filters.callback_data import CallbackData


class WishlistCallback(CallbackData, prefix="wishlist"):
    wishlist_id: int
    action: str
    item_id: Optional[str]


class ItemCallback(CallbackData, prefix="item"):
    wishlist_id: int
    item_id: int
    action: str
