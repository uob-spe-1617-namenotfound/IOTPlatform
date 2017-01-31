import requests
r = requests.get('https://mihome4u.co.uk/api/v1/devices/list', auth=('bc15050@mybristol.ac.uk', 'test1234'))
print(r.content)