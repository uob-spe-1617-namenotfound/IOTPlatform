import requests
from data_model import model
from data_model.tempcron import schedule_cron_job


def get_last_temp():
    r = requests.get("http://localhost:5010/read")
    x = r.json().get('data')
    thermostat = model.Device(1, 2, 3, "Benny's Thermostat", "thermostat", 1, 25.0, 20, 0)
    print("last temperature = %.2f" % thermostat.last_temp)
    temp = x.get('temperature')
    thermostat.last_temp = temp

    print("current temperature = %.2f" % thermostat.last_temp)

schedule_cron_job()
