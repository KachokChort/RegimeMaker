import requests
import datetime

date = datetime.date.today().strftime("%Y-%m-%d")

params = {"user": "Tima",
          "password": "bacuk22q",
          "selected_date": "2025-12-04",
          "duty_name": "Pancake 3"}
response = requests.post("http://127.0.0.1:8001/duty/", json=params)


j = response.json()
print(j)
#print(j[0] - j[1])