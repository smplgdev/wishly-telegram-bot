from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from src.utils.send_message_to_admin import send_message_to_admin
from src.utils.sending_messages_to_user import week_before_party


def set_scheduled_jobs(
        scheduler: AsyncIOScheduler,
        bot: Bot,
        *args,
        **kwargs,
):
    scheduler.add_job(send_message_to_admin, CronTrigger(hour=7, minute=57), args=(bot,))
    scheduler.add_job(week_before_party, CronTrigger(hour=8, minute=2), args=(bot,))
