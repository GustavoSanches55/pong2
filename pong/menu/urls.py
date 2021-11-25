from django.urls import path
from django.urls.conf import include
from menu import views

urlpatterns = [
    path("", views.index, name="index"),
    path("modos", views.modos, name="modos"),
]
