import requests

params = {"name": "My purpose",
          "user": "Timoha",
          "password": "12345",
          "descriptions": """Become more strong than you now.
Become more clever than you now.
Become more social than you now.
Become more sage than you now.
Become more rich than you now."""
          }
response = requests.post("http://127.0.0.1:8001/create_note/", json=params)

print(response.json())
