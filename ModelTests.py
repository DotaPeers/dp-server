import requests

url = "https://api.opendota.com/api/players/154605920/wl"

for i in range(70):
    r = requests.get(url)
    print(r)
    print(r.content)
