from django.shortcuts import render, reverse
from django.http import HttpResponse, Http404
from django.http.response import HttpResponseRedirect
import pandas as pd
from menu.models import Jogador, Partida
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np



def index(request):
    players = pd.DataFrame( Jogador.objects.all().values() )
    matches = pd.DataFrame( Partida.objects.all().values() )

    players, matches, graf1, graf2, graf3, graf4 = analise(players, matches)

    # filtragem dos dados relevantes pra ficar bonitinho no html
    players = players[['nome', 'rank', 'idade', 'email', 'hash_senha']]
    matches = matches[['p1', 'p2', 'score1', 'score2', 'rank', 'nome']]
    matches = matches.sort_values(by='p1')
    
    mydict = {
        "players": players.head(10).to_html(col_space=70,justify='center'),
        "matches": matches.head(10).to_html(col_space=70,justify='center'),
        "graf1": graf1,
        "graf2": graf2,
        "graf3": graf3,
        "graf4": graf4,
    }
    return render(request,"laguardia/index.html", context=mydict)

def analise(players, matches):

    # Corrige a base pra deixar ela idêntica aos csvs
    players.reset_index(inplace=True)
    players = players.rename(columns = {"mmr":"rank"})

    matches = pd.merge(matches, players, left_on="p1", right_on="index")

    # cria os gráficos
    mpl.style.use('dark_background')
    graf1 = grafico1(players)
    graf2 = grafico2(matches)
    graf3 = grafico3(matches)
    graf4 = grafico4(players, matches)

    return players, matches, graf1, graf2, graf3, graf4

def grafico1(players):
    return players['rank'].hist(bins=30, color='#8603ff')

def grafico2(matches):
    matches['venceu'] = matches['score1'] > matches['score2']
    
    return matches[['rank', 'idade', 'venceu']].plot(x='rank', y='idade', kind='scatter', c='#8603ff')

def grafico3(matches):
    col = matches['venceu'].map({True:'#9119ff', False:'#ff6619'})
    return matches[['rank', 'idade', 'venceu']].plot(x='rank', y='idade', kind='scatter', c=col)

def grafico4(players, matches):
    rank_p2 = players[['index', 'rank']].rename(columns={'rank':'rank p2'})

    matches2 = pd.merge(matches, rank_p2, left_on="p2", right_on="index")
    matches2['p1_venceu'] = matches2['score1'] > matches2['score2']

    col = matches2['p1_venceu'].map({True:'#9119ff', False:'#ff6619'})
    return matches2[['rank', 'rank p2', 'p1_venceu']].plot(x='rank', y='rank p2', kind='scatter', c=col)