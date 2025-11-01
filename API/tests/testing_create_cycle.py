import requests


params = {"name": "Mathematic3",
          "user": "Timoha",
          "password": "12345",
          "days_count": "7",
          "pause": "7",
          "start_at": "2025-10-28",
          "descriptions": [
              "Algebra: complete 3 examples.",
              "Geometry: complete 3 examples.",
              "Math Analys: read book 1 hour.",
              "Nothing: You can do that what you want.",
              "Algebra: complete 3 examples.",
              "Geometry: complete 3 examples.",
              "Math Analys: read book 1 hour.",
          ]}
response = requests.post("http://127.0.0.1:8000/create_cycle/", json=params)

print(response.json())