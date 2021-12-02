from django.urls import path
from django.urls.conf import include
from sanches import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
app_name = 'sanches'

urlpatterns = [
    path('', views.index, name='index'),
]
