from django.shortcuts import render, HttpResponse, redirect
import requests


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
    print(username, password)
    params = {"username": username,
              "password": password}
    response = requests.post("http://127.0.0.1:8001/user/", json=params)
    if "error" in response.json():
        return redirect("main_app:register")
    return render(request, "profile.html")
