from django.shortcuts import render, reverse
from django.http import HttpResponse, Http404
from django.http.response import HttpResponseRedirect

# Create your views here.
def index(request):
    return render(request,"menu/index.html")

def modos(request):
    return render(request,"menu/modos.html")

def leaderboards(request):
    return render(request,"menu/leaderboard.html")

def login(request):
    return render(request,"menu/login.html")
    
def modos_explicacao(request):
    return render(request,"menu/modos_explicacao.html")

def profile(request):
    return render(request,"menu/profile.html")

def jogo(request):
    return render(request, "PONG/PONG.html")
