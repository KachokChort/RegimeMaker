import requests


params = {"user": "Timoha",
          "password": "12345",}
response = requests.post("http://127.0.0.1:8000/get_notes/", json=params)

print(response.json())