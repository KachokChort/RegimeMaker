import requests
import datetime

date = datetime.date.today().strftime("%Y-%m-%d")

params = {"user": "Timoha",
          "password": "12345",
          "day": "2025-11-01"}
response = requests.post("http://127.0.0.1:8001/day/", json=params)


j = response.json()
print(j)
#print(j[0] - j[1])