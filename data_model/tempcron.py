from crontab import CronTab

cron = CronTab()

job = cron.new(command='C:\SPE\IOTPlatform\dummy_temperature_sensor\__init__.py')

job.minute.every(15)

