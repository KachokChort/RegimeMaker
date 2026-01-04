from django.urls import path
from . import views

app_name = "main_app"
urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("profile/", views.profile, name="profile"),
    path("create_cycle/", views.create_cycle, name="create_cycle"),
    path("create_note/", views.create_note, name="create_note"),
    path("delete_cycle/", views.delete_cycle, name="delete_cycle"),
    path("delete_note/", views.delete_note, name="delete_note"),
    path("day/", views.day, name="day"),
    path("duty/", views.duty, name="duty"),
    path("analyze/", views.analyze, name="analyze"),
]
