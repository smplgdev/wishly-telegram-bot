from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src import strings


class GetKeyboardMarkup:
    @staticmethod
    def start(user_name: str):
        return ReplyKeyboardMarkup(keyboard=[
            [
                KeyboardButton(text=strings.create_wishlist),
                KeyboardButton(text=strings.my_wishlists),
            ],
            [
                KeyboardButton(text=strings.gift_ideas),
                KeyboardButton(text=strings.find_friends_wishlist),
            ],
            [
                # KeyboardButton(text=strings.settings)
                KeyboardButton(text=strings.visible_name_button_text(user_name))
            ]
        ], resize_keyboard=True)

    @staticmethod
    def skip():
        return ReplyKeyboardMarkup(keyboard=[
            [
                KeyboardButton(text=strings.skip_stage)
            ]
        ], resize_keyboard=True)
