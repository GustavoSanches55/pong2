from django.shortcuts import render
from menu.models import Jogador, Partida
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.style.use('default')

def index(request):
    db_values = Jogador.objects.all().values()
    df_players = pd.DataFrame(db_values)
    df_players = df_players[["nome","mmr","idade","email"]]

    db_values  = Partida.objects.all().values()
    df_matches = pd.DataFrame(db_values)
    df_matches = df_matches[["p1","p2","score1","score2","tempo_s"]].rename(columns={"tempo_s":"tempo"})

    load_mpl_plot_style_params()
    
    df_matches_with_draw = df_matches.copy()
    df_matches = df_matches[df_matches["score1"]!=df_matches["score2"]].reset_index(drop = True)
    df_matches["p1_venceu"] = (df_matches["score1"]>df_matches["score2"])
    
    df_players["vitorias"] = 0
    df_players["partidas-jogadas"] = 0
    for i in range(df_matches.shape[0]):
        linha = df_matches.iloc[i]
        win = linha["p1_venceu"].copy()
        p1 = linha["p1"].copy()
        p2 = linha["p2"].copy()
        if win:
            n = df_players.loc[p1,"vitorias"].copy() + 1
            df_players.loc[p1,"vitorias"] = n
        else:
            n = df_players.loc[p2,"vitorias"].copy() + 1
            df_players.loc[p2,"vitorias"] = n
        n = df_players.loc[p1,"partidas-jogadas"].copy() + 1
        df_players.loc[p1,"partidas-jogadas"] = n

        n = df_players.loc[p2,"partidas-jogadas"].copy() + 1
        df_players.loc[p2,"partidas-jogadas"] = n

    df_players["derrotas"]=df_players["partidas-jogadas"]-df_players["vitorias"]
    df_players["perc_vit"]=df_players["vitorias"]/df_players["partidas-jogadas"]
    
    df_derrotas = df_players.sort_values(by=["derrotas"],ascending=False).head(10)

    path="plots/treuke_fig_1"
    plot_dist_derrotas(df_players["derrotas"],path)
    fig_dist_derrotas = path+".png"

    path="plots/treuke_fig_2"
    plot_scatter(df_players["idade"],df_players["perc_vit"],path,"idade")
    fig_idade_sucesso = path+".png"

    path="plots/treuke_fig_3"
    plot_scatter(df_players["mmr"],df_players["perc_vit"],path,"mmr")
    fig_mmr_sucesso = path+".png"

    path="plots/treuke_fig_4"
    plot_mmr_tempo(df_matches_with_draw,df_players, path)
    fig_mmr_tempo = path+".png"

    mydict = {
        "df_derrotas": df_derrotas.to_html(col_space=70,justify='center'),
        "fig_dist_derrotas": fig_dist_derrotas,
        "fig_idade_sucesso": fig_idade_sucesso,
        "fig_mmr_sucesso": fig_mmr_sucesso,
        "fig_mmr_tempo": fig_mmr_tempo
    }
    
    return render(request,"treuke/analise_treuke.html", context=mydict)

def load_mpl_plot_style_params():
    matplotlib.rcParams['axes.facecolor'] = "#FFFFFF00"
    matplotlib.rcParams['figure.facecolor'] = "#FFFFFF00"
    matplotlib.rcParams['text.color'] = "white"
    matplotlib.rcParams['axes.labelcolor'] = "white"
    matplotlib.rcParams['xtick.color'] = "white"
    matplotlib.rcParams['ytick.color'] = "white"

def plot_dist_derrotas(data,path):
    plt.hist(data,50, facecolor="#254bb1")
    plt.xlabel('N. Derrotas')
    plt.ylabel('Frequencia')
    plt.title('Distribuição de derrotas')
    path = r"static/" + path
    plt.savefig(path)
    plt.close()

def plot_scatter(valor,perc_vit,path,assunto):
    plt.scatter(valor,perc_vit, color="#52219a")
    plt.xlabel(assunto)
    plt.ylabel('Taxa de vitoria')
    plt.title('Relação entre '+assunto+' e sucesso')
    path = r"static/" + path
    plt.savefig(path)
    plt.close()

def plot_mmr_tempo(matches, players, path):
    df_matches = matches.copy()
    df = pd.merge(df_matches, players.reset_index(), left_on="p1", right_on="index")[["p1","p2","score1","score2","tempo","nome","mmr"]]
    df.rename(columns={"nome":"p1_nome","mmr":"p1_mmr"}, inplace=True)
    df = pd.merge(df, players.reset_index(), left_on="p2", right_on="index")[["p1","p2","score1","score2","tempo","p1_nome","p1_mmr","nome","mmr"]]
    df.rename(columns={"nome":"p2_nome","mmr":"p2_mmr"}, inplace=True)
    df["diferenca"] = abs(df["p1_mmr"] - df["p2_mmr"])

    plt.xlabel('Tempo em segundos')
    plt.ylabel('Diferença de mmr')
    plt.title('Duração de partidas X desnível de mmr')

    plt.scatter(df["tempo"],df["diferenca"],color="#254bb1" )
    
    path = r"static/" + path
    plt.savefig(path)
    plt.close()