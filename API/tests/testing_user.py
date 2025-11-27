import requests

data = {"username": "Timoha",
        "password": "12345"}
response = requests.post("http://127.0.0.1:8001/user/", json=data)

print(response.json())
