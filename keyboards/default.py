from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from src import strings


class GetKeyboardMarkup:
    @staticmethod
    def start(
            user_name: str,
    ):
        builder = ReplyKeyboardBuilder()
        builder.row(
            KeyboardButton(text=strings.create_wishlist),
            KeyboardButton(text=strings.my_wishlists)
        )
        builder.row(
            KeyboardButton(text=strings.gift_ideas),
            KeyboardButton(text=strings.find_friends_wishlist),
        )
        builder.row(
            KeyboardButton(text=strings.visible_name_button_text(user_name)),
        )
        return builder.as_markup(resize_keyboard=True)

    @staticmethod
    def skip():
        return ReplyKeyboardMarkup(keyboard=[
            [
                KeyboardButton(text=strings.skip_stage)
            ]
        ], resize_keyboard=True)
