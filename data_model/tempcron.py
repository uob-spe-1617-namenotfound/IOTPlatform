from crontab import CronTab

cron = CronTab()

job = cron.new(command='__init__.py')

job.minute.every(15)

