import requests
import json

# def get_last_temp():
#     r = requests.get("http://localhost:5010/read")
#     x = r.json().get('data')
#     thermostat = model.Device(1, 2, 3, "Benny's Thermostat", "thermostat", 1, 25.0, 20, 0)
#     print("last temperature = %.2f" % thermostat.last_temp)
#     temp = x.get('temperature')
#     thermostat.last_temp = temp
#
#     print("current temperature = %.2f" % thermostat.last_temp)
#
# def get_last_timestamp():
#     r = requests.get("http://localhost:5010/thermostat/1")
#     x = r.json().get('data')
#     time = x.get('timestamp')
#     resolution = x.get('resolution')
#     timestamp1 = "Wed, 25 Jan 2017 17:15:42 GMT"
#     t1 = datetime.strptime(timestamp1, "%a, %d %b %Y %H:%M:%S %Z")
#     t2 = datetime.strptime(time, "%a, %d %b %Y %H:%M:%S %Z")
#     print(timestamp1)
#     print(time)
#     difference = t2 - t1
#     print(difference.seconds)
#     if difference.seconds > resolution:
#         print("DEVICE BROKEN")
#

id = {'id': 46865}
dev = requests.get('https://mihome4u.co.uk/api/v1/subdevices/list', auth=('bc15050@mybristol.ac.uk', 'test1234'))
power_on = requests.get('https://mihome4u.co.uk/api/v1/subdevices/power_on', auth=('bc15050@mybristol.ac.uk', 'test1234'), json=id)
print(dev.content)
print(power_on.content)

