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
    colunas = ['p1','p2','score1','score2','rankp1','rankp2','media_rank','cat_p1','cat_p2','cat_partida','c']

    item = Jogador.objects.all().values()
    jogadores = pd.DataFrame(item)

    item2 = Partida.objects.all().values()
    partidas = pd.DataFrame(item2)

    load_mpl_plot_style_params()
    adiciona_colunas(jogadores,partidas)

    partidas = partidas[colunas]

    
    # Código para salvar imagem do graf2
    partidas_agrupadas = partidas.groupby(partidas["cat_p1"]).mean().round(2)
    path=r"static/plots/sanches_fig_1.png"
    graf2(partidas_agrupadas,path)

    # Código para salvar imagem do graf1
    path=r"static/plots/sanches_fig_2.png"
    graf1(partidas,path)

    por_jogador = partidas.groupby("p1").mean().sort_values('score1', ascending=False)

    descricao = partidas.describe().round(2)

    mydict = {
        "partidas": partidas.head(10).to_html(col_space=70,justify='center'),
        "descricao": descricao.to_html(col_space=70,justify='center'),
        "por_jogador": por_jogador.head(10).to_html(col_space=70,justify='center')
    }
    return render(request,"sanches/index.html", context=mydict)



def adiciona_colunas(jogadores, partidas):

    partidas['rankp1'] = partidas.p1.map(jogadores['mmr'])
    partidas['rankp2'] = partidas.p2.map(jogadores['mmr'])

    labels = ["0 a 20", "20 a 40", "40 a 60", "60 a 80", "80 a 100"]

    partidas['media_rank'] = (partidas['rankp1']+partidas['rankp2'])/2

    partidas["cat_p1"] = partidas['rankp1']
    partidas["cat_p2"] = partidas['rankp2']
    partidas["cat_partida"] = partidas['media_rank']
    partidas["cat_p1"] = pd.cut(partidas['rankp1'], 5, labels=labels)
    partidas["cat_p2"] = pd.cut(partidas['rankp2'], 5, labels=labels)
    partidas["cat_partida"] = pd.cut(partidas['cat_partida'], 5, labels=labels)

    partidas['media_rank'] = (partidas['rankp1']+partidas['rankp2'])/2

    partidas["scores_possiveis"] = partidas["score1"]

    colors = ['#EB0413', '#D020F5', '#4328DE', '#208DF5', '#1EEBC6']
    partidas['c'] = partidas.cat_partida.map({labels[0]:colors[0],labels[1]:colors[1],labels[2]:colors[2],labels[3]:colors[3],labels[4]:colors[4]})




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


def graf1(partidas,path):
    # definitions for the axes
    left, width = 0.1, 0.65
    bottom, height = 0.1, 0.65
    spacing = 0.005

    rect_scatter = [left, bottom, width, height]
    rect_histx = [left, bottom + height + spacing, width, 0.2]
    rect_histy = [left + width + spacing, bottom, 0.2, height]

    # start with a square Figure
    fig = plt.figure(figsize=(8, 8), facecolor="#1f1f1f")

    ax = fig.add_axes(rect_scatter)
    plt.xlabel("Pontos jogador 1")
    plt.ylabel("Pontos jogador 2")
    ax_histx = fig.add_axes(rect_histx, sharex=ax)
    ax_histy = fig.add_axes(rect_histy, sharey=ax)

    # use the previously defined function
    scatter_hist(partidas, partidas["score1"],partidas["score2"], ax, ax_histx, ax_histy)

    plt.xlabel("Pontos jogador 1")
    plt.ylabel("Pontos jogador 2")
    fig.suptitle('Grafico de distribuição das pontuações por partida', fontsize=16)

    plt.savefig(path)
    plt.close()


def graf2(partidas_agrupadas,path):

    fig = plt.figure(figsize=(8, 8), facecolor="#1f1f1f00")

    # left, width = 0.1, 0.65
    # bottom, height = 0.1, 0.65

    # rect_scatter = [left, bottom, width, height]

    ax = fig.add_axes([0.1,0.1,0.85,0.85])

    ax.plot(partidas_agrupadas["score1"], c='#208DF5')
    ax.plot(partidas_agrupadas["score2"], c='#D020F5')

    ax.legend(['Jogador 1', 'Jogador 2'])

    plt.savefig(path)
    plt.close()



def load_mpl_plot_style_params():
    mpl.rcParams['axes.facecolor'] = "#FFFFFF00"
    mpl.rcParams['figure.facecolor'] = "#FFFFFF00"
    mpl.rcParams['text.color'] = "white"
    mpl.rcParams['axes.labelcolor'] = "white"
    mpl.rcParams['xtick.color'] = "white"
    mpl.rcParams['ytick.color'] = "white"
    mpl.rcParams['legend.facecolor'] = "#FFFFFF00"
    mpl.rcParams['legend.framealpha'] = "0"
    # mpl.rcParams['legend.frameon'] = True



