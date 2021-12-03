from django.shortcuts import render, reverse
from django.http import HttpResponse, Http404
from django.http.response import HttpResponseRedirect
import pandas as pd
from menu.models import Jogador, Partida
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

# Create your views here.
def index(request):
    item = Jogador.objects.all().values()
    jogadores = pd.DataFrame(item)

    item2 = Partida.objects.all().values()
    partidas = pd.DataFrame(item2)
    
    adiciona_colunas(jogadores,partidas)
    # graf1(partidas)

    # partidas_agrupadas = partidas.groupby(partidas["categorias_p1"]).mean().round(2)
    # graf2(partidas_agrupadas)

    por_jogador = partidas.groupby("p1").mean().sort_values('score1', ascending=False)

    mydict = {
        "partidas": partidas.head(10).to_html(),
        "jogadores": jogadores.head(10).to_html(),
        "por_jogador": por_jogador.head(10).to_html()
    }
    return render(request,"sanches/index.html", context=mydict)


def index_sanches(request):
    item = Jogador.objects.all().values()
    jogadores = pd.DataFrame(item)

    item2 = Partida.objects.all().values()
    partidas = pd.DataFrame(item2)
    
    adiciona_colunas(jogadores,partidas)
    # graf1(partidas)

    # partidas_agrupadas = partidas.groupby(partidas["categorias_p1"]).mean().round(2)
    # graf2(partidas_agrupadas)

    por_jogador = partidas.groupby("p1").mean().sort_values('score1', ascending=False)

    mydict = {
        "partidas": partidas.head(10).to_html(),
        "jogadores": jogadores.head(10).to_html(),
        "por_jogador": por_jogador.head(10).to_html()
    }
    return render(request,"sanches/index.html", context=mydict)



def adiciona_colunas(jogadores, partidas):

    partidas['rankp1'] = partidas.p1.map(jogadores['mmr'])
    partidas['rankp2'] = partidas.p2.map(jogadores['mmr'])

    labels = ["0 a 20", "20 a 40", "40 a 60", "60 a 80", "80 a 100"]

    partidas['media_rank'] = (partidas['rankp1']+partidas['rankp2'])/2

    partidas["categorias_p1"] = partidas['rankp1']
    partidas["categorias_p2"] = partidas['rankp2']
    partidas["categoria_partida"] = partidas['media_rank']
    partidas["categorias_p1"] = pd.cut(partidas['rankp1'], 5, labels=labels)
    partidas["categorias_p2"] = pd.cut(partidas['rankp2'], 5, labels=labels)
    partidas["categoria_partida"] = pd.cut(partidas['categoria_partida'], 5, labels=labels)

    partidas['media_rank'] = (partidas['rankp1']+partidas['rankp2'])/2

    partidas["scores_possiveis"] = partidas["score1"]

    colors = ['#EB0413', '#D020F5', '#4328DE', '#208DF5', '#1EEBC6']
    partidas['c'] = partidas.categoria_partida.map({labels[0]:colors[0],labels[1]:colors[1],labels[2]:colors[2],labels[3]:colors[3],labels[4]:colors[4]})

    return partidas



def scatter_hist(partidas, x, y, ax, ax_histx, ax_histy):
    # no labels
    ax_histx.tick_params(axis="x", labelbottom=False)
    ax_histy.tick_params(axis="y", labelleft=False)

    # the scatter plot:
    ax.scatter(x, y, c=partidas["c"], alpha=0.5)
    

    # now determine nice limits by hand:
    binwidth = 0.25
    xymax = max(np.max(np.abs(x)), np.max(np.abs(y)))
    lim = (int(xymax/binwidth) + 1) * binwidth

    bins = np.arange(0, lim + binwidth, binwidth)
    ax_histx.hist(x, bins=bins)
    ax_histy.hist(y, bins=bins, orientation='horizontal')

def graf1(partidas):
    # definitions for the axes
    left, width = 0.1, 0.65
    bottom, height = 0.1, 0.65
    spacing = 0.005

    rect_scatter = [left, bottom, width, height]
    rect_histx = [left, bottom + height + spacing, width, 0.2]
    rect_histy = [left + width + spacing, bottom, 0.2, height]

    # plt.style.use('dark_background')

    # start with a square Figure
    fig = plt.figure(figsize=(8, 8), facecolor="#1f1f1f")

    ax = fig.add_axes(rect_scatter)
    plt.xlabel("Pontos jogador 1")
    plt.ylabel("Pontos jogador 2")
    ax_histx = fig.add_axes(rect_histx, sharex=ax)
    ax_histy = fig.add_axes(rect_histy, sharey=ax)

    # use the previously defined function
    scatter_hist(partidas, partidas["score1"],partidas["score2"], ax, ax_histx, ax_histy)

    mpl.rcParams['axes.facecolor'] = "#1f1f1f"
    mpl.rcParams['figure.facecolor'] = "#1f1f1f"
    mpl.rcParams['text.color'] = "white"
    mpl.rcParams['axes.labelcolor'] = "white"
    mpl.rcParams['xtick.color'] = "white"
    mpl.rcParams['ytick.color'] = "white"


    plt.xlabel("Pontos jogador 1")
    plt.ylabel("Pontos jogador 2")
    fig.suptitle('Grafico de distribuição das pontuações por partida', fontsize=16)

    plt.savefig('imagem')


def graf2(partidas_agrupadas):
        
    mpl.rcParams['axes.facecolor'] = "#1f1f1f00"
    mpl.rcParams['figure.facecolor'] = "#1f1f1f00"
    mpl.rcParams['text.color'] = "white"
    mpl.rcParams['axes.labelcolor'] = "white"
    mpl.rcParams['xtick.color'] = "white"
    mpl.rcParams['ytick.color'] = "white"

    fig = plt.figure(figsize=(8, 8), facecolor="#1f1f1f00")

    ax = fig.add_axes(rect_scatter)

    ax.plot(partidas_agrupadas["score2"], c=colors[3])
    ax.plot(partidas_agrupadas["score1"], c=colors[1])

    ax.legend(['Jogador 1', 'Jogador 2'])


