import requests


params = {"username": "Tima",
          "password": "12345"}
response = requests.post("http://127.0.0.1:8000/users/", json=params)

print(response.json())
