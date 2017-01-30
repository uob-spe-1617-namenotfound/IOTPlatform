from data_model.last_temp import get_last_temp
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

scheduler = BackgroundScheduler(daemon=False)
scheduler.start()


def schedule_cron_job():
    scheduler.add_job(
        func=get_last_temp,
        trigger=IntervalTrigger(seconds=2),
        id='get_last_temp',
        name='Get last temperature for dummy thermostat',
        replace_existing=True)

