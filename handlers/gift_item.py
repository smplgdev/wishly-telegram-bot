from aiogram import Router, F, types

from database.pgcommands.commands import ItemCommand, UserCommand
from keyboards.callback_factories import ItemCallback
from keyboards.inline import GetInlineKeyboardMarkup
from src import strings

router = Router()


@router.callback_query(ItemCallback.filter(F.action == 'gift'))
async def gift_item_handler(call: types.CallbackQuery, callback_data: ItemCallback):
    count_gifts = await UserCommand.count_user_gifts(call.from_user.id)
    if count_gifts >= 3:
        await call.answer(strings.item_limit, show_alert=True)
        return
    item_id = callback_data.item_id
    item = await ItemCommand.gift(call.from_user.id, item_id)
    markup = GetInlineKeyboardMarkup.item_markup(item)
    await call.message.edit_reply_markup(markup)
    if item:
        await call.answer(strings.item_gifted, show_alert=True)
    if not item:
        await call.answer(strings.seems_that_someone_gift_it, show_alert=True)
