from django.urls import path
from django.urls.conf import include
from treuke import views

# app_name = "treuke"

urlpatterns = [
    path('', views.index, name='treuke-analise'),
]
