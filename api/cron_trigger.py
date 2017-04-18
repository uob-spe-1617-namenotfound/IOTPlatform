from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

import logging
scheduler = BackgroundScheduler(daemon=False)
scheduler.start()


def check_all_triggers():
    from main import api
    logging.debug("Checking trigger readings")
    api.trigger_repository.check_all_triggers()


def setup_cron():
    scheduler.add_job(
        func=check_all_triggers,
        trigger=IntervalTrigger(seconds=300),
        id='check_all_triggers',
        name='Checking all trigger readings',
        replace_existing=True)