from django.shortcuts import render, reverse
from django.http import HttpResponse, Http404
from django.http.response import HttpResponseRedirect
import pandas as pd
from menu.models import Jogador, Partida

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

def salvar_csv(request):
    i=0
    
    # df = pd.read_csv("csv/jogadores.csv")
    # for linha in df.itertuples():
    #     nome = linha[2]
    #     mmr = linha[3]
    #     idade = linha[4]
    #     email = linha[5]
    #     hash_senha = linha[6]

    #     player = Jogador(nome=nome, mmr=mmr, idade=idade, email=email, hash_senha=hash_senha)
    #     player.save()
    #     i+=1

    # df = pd.read_csv("csv/partidas.csv")
    # for linha in df.itertuples():
    #     p1 = linha[1]
    #     p2 = linha[2]
    #     score1 = linha[3]
    #     score2 = linha[4]
    #     tempo_s = linha[5]

    #     match = Partida(p1=p1, p2=p2, score1=score1, score2=score2, tempo_s=tempo_s)
    #     match.save()
    #     i+=1
    aaaa = ""
    for coisa in Partida.objects.all():
        aaaa+= str(coisa.p1)+"<br>"

    return HttpResponse(str("EIEIEIEIEII: "+aaaa))
