import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from bot.utils.scheduled_jobs.make_wishlists_inactive import make_old_wishlists_inactive
from bot.utils.scheduled_jobs.message_party_is_soon import party_is_soon_message

ONE_HOUR_IN_SECONDS = 60*60


def clean_scheduled_jobs(
        scheduler: AsyncIOScheduler,
):
    scheduler.remove_all_jobs()


def set_scheduled_jobs_once(
        scheduler: AsyncIOScheduler,
):
    scheduled_jobs_ids = [job.id for job in scheduler.get_jobs()]

    make_old_wishlists_inactive_id = "make_old_wishlists_inactive"
    if make_old_wishlists_inactive_id not in scheduled_jobs_ids:
        scheduler.add_job(
            make_old_wishlists_inactive,
            CronTrigger(hour=2, minute=0),
            id=make_old_wishlists_inactive_id,
            misfire_grace_time=ONE_HOUR_IN_SECONDS
        )
        logging.info('Scheduled job "make_old_wishlists_inactive" added')

    send_party_is_soon_message_id = "party_is_soon_message"
    if send_party_is_soon_message_id not in scheduled_jobs_ids:
        scheduler.add_job(
            party_is_soon_message,
            CronTrigger(hour=15, minute=35),
            id=send_party_is_soon_message_id,
            misfire_grace_time=ONE_HOUR_IN_SECONDS,
        )
        logging.info('Scheduled job "party_is_soon_message" added')
