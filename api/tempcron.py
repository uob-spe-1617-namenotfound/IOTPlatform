from data_model.last_temp import get_last_timestamp
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

scheduler = BackgroundScheduler(daemon=False)
scheduler.start()


def schedule_cron_job():
    scheduler.add_job(
        func=get_last_timestamp,
        trigger=IntervalTrigger(seconds=2),
        id='get_last_temp',
        name='Get last timestamp for the faulty thermostat',
        replace_existing=True)

schedule_cron_job()