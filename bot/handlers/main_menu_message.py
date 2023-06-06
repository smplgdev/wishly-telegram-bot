from aiogram import Bot

from keyboards.default import GetKeyboardMarkup
import strings


async def main_menu_send_message(
        bot: Bot,
        user_tg_id: int,
        user_name: str,
) -> None:
    await bot.send_message(
        chat_id=user_tg_id,
        text=strings.start_text(
            user_first_name=user_name
        ),
        reply_markup=GetKeyboardMarkup.start(
            user_name=user_name,
        )
    )
