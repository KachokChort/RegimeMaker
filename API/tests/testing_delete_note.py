import requests


params = {"note_name": "My purpose",
          "user": "Timoha",
          "password": "12345",}
response = requests.post("http://127.0.0.1:8000/delete_note/", json=params)

print(response.json())