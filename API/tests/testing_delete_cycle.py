import requests


params = {"cycle_name": "Mathematic",
          "user": "Timoha",
          "password": "12345",}
response = requests.post("http://127.0.0.1:8000/delete_cycle/", json=params)

print(response.json())