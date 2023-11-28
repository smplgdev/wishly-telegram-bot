from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from bot import strings


def start_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text=strings.create_wishlist),
        KeyboardButton(text=strings.my_wishlists)
    )
    builder.row(
        KeyboardButton(text=strings.gift_ideas),
        # KeyboardButton(text=strings.find_friends_wishlist),
    )
    return builder.as_markup(resize_keyboard=True)


def skip_stage_keyboard():
    return ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text=strings.skip_stage)
        ]
    ], resize_keyboard=True)
