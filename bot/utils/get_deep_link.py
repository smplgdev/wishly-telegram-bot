import re

from bot.utils.types import ListTypes


def get_deep_link(message_text: str) -> tuple[ListTypes, str] | tuple[bool, bool]:
    is_hashcode = re.fullmatch(r'^/start (wl|sl)_[A-Z0-9]{4,6}$', message_text)
    if not is_hashcode:
        return False, False
    separated_str = message_text.split(" ")[-1].split("_")
    if separated_str[0] == 'wl':
        return ListTypes.WISHLIST, separated_str[-1]
    elif separated_str[0] == 'sl':
        return ListTypes.SECRET_LIST, separated_str[-1]
