from typing import Optional
from enum import Enum

from pydantic import BaseModel, conlist, Field

from aiogram.filters.callback_data import CallbackData


class SimpleCalAct(str, Enum):
    ignore = 'IGNORE'
    prev_y = 'PREV-YEAR'
    next_y = 'NEXT-YEAR'
    prev_m = 'PREV-MONTH'
    next_m = 'NEXT-MONTH'
    cancel = 'CANCEL'
    today = 'TODAY'
    day = 'DAY'


class DialogCalAct(str, Enum):
    ignore = 'IGNORE'
    set_y = 'SET-YEAR'
    set_m = 'SET-MONTH'
    prev_y = 'PREV-YEAR'
    next_y = 'NEXT-YEAR'
    cancel = 'CANCEL'
    start = 'START'
    day = 'SET-DAY'


class CalendarCallback(CallbackData, prefix="calendar"):
    act: str
    year: Optional[int] = None
    month: Optional[int] = None
    day: Optional[int] = None


class SimpleCalendarCallback(CalendarCallback, prefix="simple_calendar"):
    act: SimpleCalAct


class DialogCalendarCallback(CalendarCallback, prefix="dialog_calendar"):
    act: DialogCalAct


class CalendarLabels(BaseModel):
    "Schema to pass labels for calendar. Can be used to put in different languages"
    days_of_week: conlist(str, max_length=7, min_length=7) = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    months: conlist(str, max_length=12, min_length=12) = [
        "Янв", "Фев", "Мар", "Апр", "Май", "Июн", "Июл", "Авг", "Сен", "Окт", "Ноя", "Дек"
    ]
    cancel_caption: str = Field(default='Cancel', description='Caprion for Cancel button')
    today_caption: str = Field(default='Today', description='Caprion for Cancel button')


HIGHLIGHT_FORMAT = "[{}]"


def highlight(text):
    return HIGHLIGHT_FORMAT.format(text)
