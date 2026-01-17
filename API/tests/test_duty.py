import requests
import datetime

date = datetime.date.today().strftime("%Y-%m-%d")

params = {"user": "Tima",
          "password": "bacuk22q",
          "selected_date": "2026-01-17",
          "duty_name": "Ronnie Coleman"}
response = requests.post("http://127.0.0.1:8001/duty/", json=params)


j = response.json()
print(j)
#print(j[0] - j[1])