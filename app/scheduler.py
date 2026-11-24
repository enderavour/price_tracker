from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.tasks import run_price_update
from datetime import datetime

scheduler = AsyncIOScheduler()

def start_scheduler():
    if not scheduler.running:
        scheduler.add_job(
            run_price_update,
            trigger="interval",
            hours=3,
            id="decathlon_price_update",
            replace_existing=True,
            max_instances=1,
            next_run_time=datetime.now()
        )

        scheduler.start()


def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown()