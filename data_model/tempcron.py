from crontab import CronTab

cron = CronTab()

job = cron.new(command='python last_temp.py')
job.minutes.every(1)
