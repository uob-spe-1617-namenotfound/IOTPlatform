from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

import logging
scheduler = BackgroundScheduler(daemon=False)
scheduler.start()


def update_all_readings():
    from main import api
    logging.debug("Updating all readings")
    api.device_repository.update_all_device_readings()


def setup_cron():
    scheduler.add_job(
        func=update_all_readings,
        trigger=IntervalTrigger(seconds=10),
        id='update_all_readings',
        name='Get all device readings',
        replace_existing=True)
