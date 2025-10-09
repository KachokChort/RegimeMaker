import requests


params = {"name": "Trainings",
          "user": "Timoha",
          "password": "12345",
          "days_count": "7",
          "descriptions": {
              "1": "Pull ups",
              "2": "Rest",
              "3": "Push ups",
              "4": "Rest",
              "5": "Legs",
              "6": "Rest",
              "7": "Static",
          }}
response = requests.post("http://127.0.0.1:8000/create_cycle/", json=params)

print(response.json())