import random

from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncSession

from bot import strings
from bot.db.models import SecretList
from bot.db.models.secret_list_participants import SecretListParticipant
from bot.db.queries.secret_list import get_secret_list_or_none_by_id, change_secret_list_status, \
    get_participant_or_none_by_id, update_participant
from bot.db.queries.users import get_user_or_none_by_id
from bot.utils.send_message import send_message


async def run_secret_list_game(
        session: AsyncSession,
        bot: Bot,
        sl_id: int = None,
):
    sl = await get_secret_list_or_none_by_id(session, sl_id=sl_id)

    user_pairs = shuffle_users(participants_ids=list(participant.id for participant in sl.participants))
    updated_participants = list()
    for participant_id, giver_participant_id in user_pairs.items():
        participant = await get_participant_or_none_by_id(session, participant_id)
        await update_participant(session, participant, giver_participant_id=giver_participant_id)
        await session.refresh(participant)
        updated_participants.append(participant)
        giver_wishlist = participant.giver_participant
        user_has_gifts: bool = len(giver_wishlist.items) > 0
        await send_message(
            bot=bot,
            user_id=participant.user.telegram_id,
            text=strings.running_secret_list_participant_text(sl_title=sl.title,
                                                              participants_count=len(sl.participants),
                                                              participant=participant,
                                                              user_has_gifts=user_has_gifts)
        )

    creator = await get_user_or_none_by_id(session, user_id=sl.creator_id)

    await send_message(
        bot=bot,
        user_id=creator.telegram_id,
        text=strings.running_secret_list_owner_text(sl=sl)
    )
    await change_secret_list_status(session, sl=sl, status="running")


def shuffle_users(participants_ids: list[int]) -> dict:
    shuffled_ids = random.sample(participants_ids, len(participants_ids))

    # Проверяем, чтобы ключи не совпадали со значениями, и если совпадают, перемешиваем значения заново
    while any(participants_ids[i] == shuffled_ids[i] for i in range(len(participants_ids))):
        shuffled_ids = random.sample(participants_ids, len(participants_ids))

    shuffled_pairs = {participants_ids[i]: shuffled_ids[i] for i in range(len(participants_ids))}

    return shuffled_pairs
