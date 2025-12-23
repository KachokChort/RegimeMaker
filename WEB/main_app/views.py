import json

from django.shortcuts import render, HttpResponse, redirect
import requests
import datetime


def index(request):
    request.session.flush()
    return render(request, "index.html", {"name": "Tayler"})


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        params = {"username": username,
                  "password": password}
        response = requests.post("http://127.0.0.1:8001/sign_up/", json=params)
        data = response.json()
        if "error" in data:
            return render(request, "register.html", context={"error": data["error"]})
        else:
            request.session["username"] = username
            request.session["password"] = password
            return redirect("main_app:profile")
    return render(request, "register.html")


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        params = {"username": username,
                  "password": password}
        response = requests.post("http://127.0.0.1:8001/user/", json=params)
        data = response.json()
        if "error" in data:
            return render(request, "login.html", context={"error": data["error"]})
        else:
            request.session["username"] = username
            request.session["password"] = password
            return redirect("main_app:profile")
    return render(request, "login.html")


def profile(request):
    username = request.session.get("username")
    password = request.session.get("password")
    duties = request.session.get("duties", {})
    selected_date = request.session.get("selected_date")

    # обработка входа
    params_1 = {"username": username,
                "password": password}
    response = requests.post("http://127.0.0.1:8001/user/", json=params_1)
    if "error" in response.json():
        return redirect("main_app:register")

    # циклы получаем
    params_cycle = {"user": username,
                    "password": password}
    response_user_cycles = requests.post("http://127.0.0.1:8001/user_cycles/", json=params_cycle)
    data = response_user_cycles.json()
    # print(data)
    if "verdict" in data:
        cycles = data.get("cycles")
    else:
        cycles = []

    # заметки получаем
    params_note = {"user": username,
                   "password": password}
    response_user_notes = requests.post("http://127.0.0.1:8001/get_notes/", json=params_note)
    data = response_user_notes.json()
    # print(data)
    if "verdict" in data:
        notes = data.get("notes")
    else:
        notes = []

    exercises = requests.post("http://127.0.0.1:8001/get_exercises/")

    exercises = exercises.json()
    # print(exercises, "----------------------------------------------")

    context = {"cycles": cycles, "notes": notes, "duties": duties, "selected_date": selected_date, "username": username,
               "exercises": exercises}
    return render(request, "profile.html", context)


def create_cycle(request):
    if request.method == "POST":
        username = request.session.get("username")
        password = request.session.get("password")

        data_cycle = request.POST.get('cycle_data')
        data_cycle = json.loads(data_cycle)

        descriptions = []
        for key, value in data_cycle.items():
            text = ""
            for exercise in value:
                text += exercise.get("name", "") + ": " + str(exercise.get("sets", ""))
            descriptions.append(text)

        params = {"name": request.POST.get("name"),
                  "user": username,
                  "password": password,
                  "days_count": int(request.POST.get("days_count")),
                  "pause": int(request.POST.get("pause")),
                  "start_at": request.POST.get("start_at"),
                  "descriptions": descriptions,
                  "data_cycle": data_cycle}

        response = requests.post("http://127.0.0.1:8001/create_cycle/", json=params)
        # print(response.json())
        if "error" in response.json():
            return HttpResponse(response.json().get("error"))
        else:
            return redirect("main_app:profile")
    elif request.method == "GET":
        return redirect("main_app:profile")


def create_note(request):
    if request.method == "POST":
        username = request.session.get("username")
        password = request.session.get("password")

        params = {"name": request.POST.get("name"),
                  "user": username,
                  "password": password,
                  "descriptions": request.POST.get("descriptions")}

        response = requests.post("http://127.0.0.1:8001/create_note/", json=params)
        if "error" in response.json():
            return HttpResponse(response.json().get("error"))
        else:
            return redirect("main_app:profile")
    elif request.method == "GET":
        return redirect("main_app:profile")


def delete_cycle(request):
    if request.method == "POST":
        username = request.session.get("username")
        password = request.session.get("password")

        params = {"cycle_name": request.POST.get("cycle_name"),
                  "user": username,
                  "password": password}

        response = requests.post("http://127.0.0.1:8001/delete_cycle/", json=params)
        if "error" in response.json():
            return HttpResponse(response.json().get("error"))
        else:
            return redirect("main_app:profile")
    return redirect("main_app:profile")


def delete_note(request):
    if request.method == "POST":
        username = request.session.get("username")
        password = request.session.get("password")

        params = {"note_name": request.POST.get("note_name"),
                  "user": username,
                  "password": password}

        response = requests.post("http://127.0.0.1:8001/delete_note/", json=params)
        # print(response.json())
        if "error" in response.json():
            return HttpResponse(response.json().get("error"))
        else:
            return redirect("main_app:profile")
    return redirect("main_app:profile")


def day(request):
    if request.method == "POST":
        username = request.session.get("username")
        password = request.session.get("password")
        selected_date = request.POST.get("day")
        print(selected_date)
        params = {"password": password,
                  "user": username,
                  "day": selected_date}

        response = requests.post("http://127.0.0.1:8001/day/", json=params)
        # print(response.json())
        if "error" in response.json():
            return HttpResponse(response.json().get("error"))
        else:
            request.session["selected_date"] = selected_date
            request.session["duties"] = response.json().get("duties")
            # print(response.json().get("duties"))
            return redirect("main_app:profile")
    return redirect("main_app:profile")


def duty(request):
    if request.method == "POST":
        username = request.session.get("username")
        password = request.session.get("password")
        selected_date = request.POST.get("selected_date")
        duty_name = request.POST.get("duty_name")
        # print(selected_date, duty_name)
        params = {"password": password,
                  "user": username,
                  "selected_date": selected_date,
                  "duty_name": duty_name}

        response = requests.post("http://127.0.0.1:8001/duty/", json=params)
        # print(response.json())
        if "error" in response.json():
            return HttpResponse(response.json().get("error"))
        else:
            request.session["duties"] = response.json().get("duties").get(selected_date)
            return redirect("main_app:profile")
    return redirect("main_app:profile")






