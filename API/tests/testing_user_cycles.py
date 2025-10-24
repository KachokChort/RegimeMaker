import requests


params = {"user": "Timoha",
          "password": "12345",}
response = requests.post("http://127.0.0.1:8000/user_cycles/", json=params)

print(response.json())