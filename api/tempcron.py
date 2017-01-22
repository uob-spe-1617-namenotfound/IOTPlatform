from crontab import CronTab

cron = CronTab()

job = cron.new(command='last_temp.py')
job.minutes.every(1)
