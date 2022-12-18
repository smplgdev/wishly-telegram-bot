from aiogram import Bot
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler


job_stores = {
    "default": RedisJobStore(
        jobs_key="dispatched_trips_jobs", run_times_key="dispatched_trips_running",
        # параметры host и port необязательны, для примера показано как передавать параметры подключения
        # host="localhost", port=6379
    )
}


def set_scheduled_jobs(
        scheduler: AsyncIOScheduler,
        bot: Bot,
):
    pass
