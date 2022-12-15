from aiogram.utils.markdown import hide_link

from database.models.User import User
from database.models.Wishlist import Wishlist


def hi_user_message(user_tg_id: int = 0):
    return f"Hi, user #{user_tg_id}"


create_wishlist = "📝 Создать вишлист"
create_wishlist_inline_button = "➕ Создать вишлист"
my_wishlists = "📚 Мои вишлисты"
gift_ideas = "🎁 Идеи для подарка"
find_friends_wishlist = "🫶 Вишлисты друзей"
find_wishlist = "🔎 Найти вишлист"
settings = "⚙️ Настройки"
gifts = "🎁 Подарки"


def start_text(user_first_name: str):
    text = f"👋 Добрый день, <b>{user_first_name}</b>!\n\nПри помощи <b>Wishly</b> вы можете создать " \
           f"свой список подарков для любого праздника или посмотреть вишлисты своих друзей и выбрать им подарок!"
    return text


not_logged_user = "Для того, чтобы продолжить, перейдите в бота!"
first_log_in = "Нажмите, чтобы продолжить"
enter_wishlist_title = "<b>Введите название вашего вишлиста</b>. " \
                       "Его увидят все, кому вы отправите вишлист. В названии можно использовать смайлики. " \
                       "<b>Важно</b>: название не должно превышать длины 64 символа!\n\n" \
                       "Например: <i>День рождения</i>, <i>Новый год</i> 🎄, <i>8 марта</i> и т.д."
go_to_wishlist = "Перейти в вишлист"
delete_item = "❌ Удалить подарок из вишлиста"
item_successfully_deleted = "Подарок успешно удалён из вишлиста"
wishlist_title_too_long = "Этот заголовок слишком длинный. Пожалуйста, введите заголовок, длиной менее 64 символов"
enter_expire_date = "Введите дату праздника в формате дд.мм.гггг" \
                    "\n\nНапример: <i>24.11.2023</i>"
go_to_bot = "Перейти в меню бота"
past_date_error = "Эта дата уже в прошлом. Введите дату, которая находится в будущем" \
            f"\n\nНапример: <i>24.11.2027</i>"

date_value_error = "Вы ввели дату в неправильном формате. " + enter_expire_date


def wishlist_successfully_created(wishlist: Wishlist):
    return f"Вишлист «<b>{wishlist.title}</b>» успешно создан!" \
           f"\n\nЕго уникальный номер: #{wishlist.hashcode}, " \
           f"он также доступен по ссылке:\nhttps://t.me/wishlyRobot?start=wl_{wishlist.hashcode}" \
           "\n\nТеперь добавь подарки, которые хочешь получить, " \
           "а затем отправь эту ссылку друзьям или выложи её в свои соцсети, "\
           "чтобы все знали, что тебе подарить!"


add_item_to_wishlist = "➕ Добавить подарок"
delete_wishlist = "🗑 Удалить вишлист"
enter_item_title = "<b>Добавляем подарок в вишлист</b>" \
             "\n\n1. Введите название подарка. Важно: оно не должно превышать 64 символа"
skip_stage = "Пропустить ⏭"
item_title_too_long = "Название подарка слишком длинное. Пожалуйста, используйте название не длиннее 64 символов"
item_description = "2. Введите <b>текстовое</b> описание вашего подарка, если это необходимо. " \
                   f"Если нет, нажмите кнопку <b>{skip_stage}</b>" \
                   "\nДлина описания не должна превышать 512 символов"

item_description_too_long = "Описание подарка слишком длинное. Пожалуйста, придумайте описание не длиннее 256 символов"
attach_item_photo = f"Отправьте фото подарка. Если фотография не требуется, нажмите кнопку {skip_stage}"


def item_info_text(title: str, description: str | None):
    text = str()
    text += f"<b>{title}</b>"
    if description:
        text += '\n\n' + description
    return text


reply_item_info_example = "Вот так выглядит карточка вашего подарка. Добавить его в список или удалить?"
apply_adding_to_wishlist = "✅ Добавить"
discard_adding_to_wishlist = "❌ Удалить"
creating_item_discard = "Создание карточки подарка успешно отменено"
creating_item_apply = "<b>Подарок успешно добавлен в вишлист</b>! " \
                      "Вы можете добавить еще подарок или вернуться в главное меню"
add_one_more_item = "Добавить еще один подарок 🎁"
main_menu = "В главное меню 🏠"


def wishlist_found_in_deep_link(wishlist: Wishlist, creator_user: User):
    text = f"Я обнаружил вишлист «<b>{wishlist.title}</b>» от пользователя {creator_user.name} в вашей ссылке!" \
           f"\n\nВы желаете перейти в этот вишлист?"
    return text


go_to_friend_wishlist = "Перейти в вишлист друга"
your_wishlists = "Список ваших вишлистов:"

item_status = {
    'free': '🟢',
    'owned': '🔴',
}

items_list = f"<b>Чтобы показать список подарков, нажмите на кнопку ниже</b>" \
             "\nЕсли рядом с подарком стоит галочка (✅), значит эту вещь уже подарит кто-то другой"

go_back = "🔙 Назад"
i_will_gift_this_item = "Я подарю это!"
someone_else_gift_it = "Этот подарок дарит кто-то другой"
item_gifted = "Успешно!"
item_limit = "К сожалению, пока что вы не можете отметить больше трёх подарков в одном вишлисте 😟"

show_items_list = "Открыть список подарков 🎁"


def wishlist_title(wishlist: Wishlist, wishlist_owner: User):
    text = f"Вишлист «{wishlist.title}» #{wishlist.hashcode}" \
           f"\nДата события: {wishlist.expiration_date.strftime('%d.%m.%Y')}" \
           f"\nАвтор: <b>{wishlist_owner.name}</b>"
    if wishlist_owner.username:
        text += f" @{wishlist_owner.username}"
    text += f"\n\nСсылка на вишлист:\nhttps://t.me/wishlyRobot?start=wl_{wishlist.hashcode}"
    return text


gift_limit_reached = "Лимит подарков достигнут! " \
                     "К сожалению, на данный момент вы не можете добавить больше 50 подарков в вишлист 😔"
settings_menu = "Вы находитесь в меню настроек. Здесь вы можете поменять отображаемое имя"
change_visible_name = "Изменить отображаемое имя: "


def visible_name_button_text(user_name: str):
    return change_visible_name + user_name


user_hasnt_added_any_items = "Здесь пока нет ни одного подарка ☹️"
edit_wishlist = "✏️ Редактировать вишлист"
what_you_want_to_do_with_wishlist = "Что вы хотите сделать с вишлистом? Выберите из списка"
are_you_sure_to_delete_wishlist = "Вы уверены, что хотите удалить вишлист?"
yes_delete = "Да, удалить 🗑"
no_delete = "Оставить"
delete_cancel = "Удаление вишлиста отменено"
delete_successful = "Вишлист успешно удалён"
send_new_name = "Отправьте в чат новое имя. " \
                "Оно будет отображаться у всех пользователей, " \
                "которые откроют ваши вишлисты. Длина имени должна быть от 1 до 64 символов"
name_too_long = "Имя, которое вы придумали, слишком длинное. Придумайте другое и напишите его в чат:"
name_successfully_changed = "Имя успешно изменено"
friends_wishlists_below = "Ниже находятся вишлисты ваших друзей 🤗\n\n" \
                          "Если вы хотите найти другой вишлист, нажмите на кнопку " + find_wishlist
enter_hashcode = "Введите хэш вишлиста друга.\n\nНапример: #ABCD1" \
                 "\n\nВажно: вы также можете найти вишлист друга, попросив у него ссылку и просто перейдя по ней"
cant_find_wishlist = "Я не могу найти этот вишлист. Пожалуйста, введите хэш в правильном формате " \
                     "(например #ABCD) или попросите ссылку у друга"
found_wishlist = "Мы нашли этот вишлист!"
seems_that_someone_gift_it = "Похоже, что этот подарок уже дарит кто-то другой 🫠" \
                             "\n\nВыберите другой подарок из списка"


def get_inline_query_message_text(
    title: str,
    description: str | bool = None,
    photo_link: str | bool = None
) -> str:
    text_parts = list()

    text_parts.append(
        f"<b>{title}</b>" + hide_link(photo_link)
    )
    if description:
        text_parts.append(
            "\n\n" + description
        )

    return "".join(text_parts)



