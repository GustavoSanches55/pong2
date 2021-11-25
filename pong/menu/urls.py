from django.urls import path
from django.urls.conf import include
from menu import views

urlpatterns = [
    path("", views.index, name="index"),
    path("modos", views.modos, name="modos"),
    path("profile", views.profile, name="profile"),
    path("login", views.login, name="login"),
    path("modos/explicacao", views.modos_explicacao, name="modos_explicacao"),
    path("leaderboards", views.leaderboards, name="leaderboards"),
]
