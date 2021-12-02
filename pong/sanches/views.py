from django.shortcuts import render, reverse
from django.http import HttpResponse, Http404
from django.http.response import HttpResponseRedirect
import pandas as pd
from menu.models import Jogador, Partida

# Create your views here.
def index(request):
    return render(request,"sanches/index.html")
