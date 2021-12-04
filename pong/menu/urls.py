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
    path("jogo", views.jogo, name="jogo"),
    path("salvar_csv", views.salvar_csv, name="salvar_csv"),
    path("analises_menu", views.analises_menu, name="analises_menu"),
    path("notas", views.notas, name="notas"),
    path(r'sanches/', include('sanches.urls',  namespace='sanches')),
    path(r'kayo/', include('kayo.urls',  namespace='kayo')),
    path(r'laguardia/', include('laguardia.urls',  namespace='laguardia')),
    # path(r'treuke/', include('treuke.urls',  namespace='treuke'))
    path(r'treuke/', include('treuke.urls'))
]
