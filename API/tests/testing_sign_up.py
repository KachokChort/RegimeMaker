import requests


params = {"username": "Timoha",
          "password": "12345"}
response = requests.post("http://127.0.0.1:8000/sign_up/", json=params)

print(response.json())
