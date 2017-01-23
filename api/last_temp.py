import requests
from api import model

r = requests.get("http://localhost:5010/read")
x = r.json().get('data')

last_temp = x.get('temperature')
thermostat = model.Device(1, 2, 3, "Benny's Thermostat", "thermostat", 1, last_temp, 20, 0)

