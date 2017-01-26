import requests
from datetime import datetime

# def get_last_temp():
#     r = requests.get("http://localhost:5010/thermostat/1")
#     x = r.json().get('data')
#     temp = x.get('temperature')
#     print("current temperature = %.2f" % temp)


def get_last_timestamp():
    r = requests.get("http://localhost:5010/thermostat/1")
    x = r.json().get('data')
    time = x.get('timestamp')
    resolution = x.get('resolution')
    timestamp1 = "Wed, 25 Jan 2017 17:15:42 GMT"
    t1 = datetime.strptime(timestamp1, "%a, %d %b %Y %H:%M:%S %Z")
    t2 = datetime.strptime(time, "%a, %d %b %Y %H:%M:%S %Z")
    print(timestamp1)
    print(time)
    difference = t2 - t1
    print(difference.seconds)
    if difference.seconds > resolution:
        print("DEVICE BROKEN")
