from django.urls import path
from django.urls.conf import include
from kayo import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = 'kayo'

urlpatterns = [
    path('', views.index, name='index'),
]
