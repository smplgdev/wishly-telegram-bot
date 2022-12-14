import io

from aiogram import types, F, Router, Bot

from database.pgcommands.commands import UserCommand, ItemCommand
from filters.admin_filter import AdminFilter
from keyboards.default import GetKeyboardMarkup
from src import strings
from src.utils.photo_link_telegraph import upload_photo

admin_router = Router()


@admin_router.message(AdminFilter(), F.text == 'update_kb')
async def send_bot_update_message(message: types.Message, bot: Bot):
    users = await UserCommand.get_all_users()
    for user in users:
        await bot.send_message(
            user.tg_id,
            "Бот обновился! Теперь просмотр списка подарков стал еще удобнее, "
            f"а вишлисты друзей доступны по нажатию одной кнопки <b>{strings.find_friends_wishlist}</b>",
            reply_markup=GetKeyboardMarkup.start(user_name="admin")
        )


@admin_router.message(AdminFilter(), F.text == 'update_pics')
async def update_pictures_admin_handler(message: types.Message, bot: Bot):
    items = await ItemCommand.get_all_items()
    for item in items:
        if not item.photo_file_id:
            continue
        msg = await bot.send_photo(
            5543936487,
            photo=item.photo_file_id,
        )
        bytes_photo = io.BytesIO()
        await bot.download(msg.photo[0], bytes_photo)
        thumb_link = await upload_photo(bytes_photo)

        bytes_photo = io.BytesIO()
        await bot.download(msg.photo[-1], bytes_photo)
        photo_link = await upload_photo(bytes_photo)

        await ItemCommand.update(
            item=item,
            photo_link=photo_link,
            thumb_link=thumb_link
        )
        await bot.send_message(
            5543936487,
            text=photo_link + '\n\n' + thumb_link,
            reply_to_message_id=msg.message_id
        )
