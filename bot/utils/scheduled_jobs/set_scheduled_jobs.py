from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from bot.utils.scheduled_jobs.make_wishlists_inactive import make_old_wishlists_inactive
from bot.utils.scheduled_jobs.message_party_is_soon import party_is_soon_message

ONE_HOUR_IN_SECONDS = 60*60


def clean_scheduled_jobs(
        scheduler: AsyncIOScheduler,
):
    # jobs_to_remove = list(filter(lambda job: job.name in ["make_old_wishlists_inactive", "party_is_soon_message"], scheduler.get_jobs()))
    scheduler.remove_all_jobs()


def set_scheduled_jobs(
        scheduler: AsyncIOScheduler,
):
    scheduler.add_job(
        make_old_wishlists_inactive,
        CronTrigger(hour=2, minute=0),
        misfire_grace_time=ONE_HOUR_IN_SECONDS
    )

    scheduler.add_job(
        party_is_soon_message,
        CronTrigger(hour=15, minute=35),
        misfire_grace_time=ONE_HOUR_IN_SECONDS,
    )
