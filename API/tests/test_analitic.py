import requests
import datetime

params = {"user": "Tima",
          "password": "bacuk22q",
          "cycle_name": "Блинчики"}
response = requests.post("http://127.0.0.1:8001/analytics/", json=params)


j = response.json()
print(j)
#print(j[0] - j[1])