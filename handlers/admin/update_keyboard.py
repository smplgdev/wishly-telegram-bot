import asyncio
import io

from aiogram import types, F, Router, Bot

from database.pgcommands.commands import UserCommand, ItemCommand
from filters.admin_filter import AdminFilter
from keyboards.default import GetKeyboardMarkup
from src import strings
from src.utils.photo_link_telegraph import upload_photo

admin_router = Router()


@admin_router.message(AdminFilter(), F.text == 'update')
async def send_bot_update_message(message: types.Message, bot: Bot):
    users = await UserCommand.get_all_users()
    cnt = 0
    for user in users:
        try:
            await bot.send_message(
                user.tg_id,
                "Бот обновился! Теперь просмотр списка подарков стал еще удобнее, "
                f"а вишлисты друзей доступны по нажатию одной кнопки <b>{strings.find_friends_wishlist}</b>",
                reply_markup=GetKeyboardMarkup.start(user_name="admin")
            )
        except Exception as e:
            print(e)
            cnt += 1
            await UserCommand.make_inactive(user_tg_id=user.tg_id)
            continue
        await asyncio.sleep(0.04)
    print("%s users banned bot" % cnt)


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
