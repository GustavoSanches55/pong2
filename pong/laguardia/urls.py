from django.urls import path
from django.urls.conf import include
from laguardia import views
app_name = 'laguardia'

urlpatterns = [
    path('', views.index, name='index'),
]
