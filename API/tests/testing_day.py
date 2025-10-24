import requests
import datetime

date = datetime.date.today().strftime("%Y-%m-%d")

params = {"user": "Timoha",
          "password": "12345",
          "day": "2025-10-24"}
response = requests.post("http://127.0.0.1:8000/day/", json=params)


j = response.json()
print(j)
#print(j[0] - j[1])