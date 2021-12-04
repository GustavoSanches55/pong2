from django.shortcuts import render, reverse
from django.http import HttpResponse, Http404
from django.http.response import HttpResponseRedirect
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from menu.models import Jogador, Partida

# Create your views here.
def tabela1():
    item2 = Partida.objects.all().values()
    partidas = pd.DataFrame(item2)


    score1_tempo = partidas.groupby("p1")[["score1", "tempo_s"]].apply(lambda x: x.sum())
    score1_tempo["tempo_s"] = score1_tempo["tempo_s"]/60
    # tempo_total = score1_tempo["tempo"].sum()
    
    return score1_tempo



def tabela2():
    item = Jogador.objects.all().values()
    jogadores = pd.DataFrame(item)

    item2 = Partida.objects.all().values()
    partidas = pd.DataFrame(item2)

    score1_tempo = partidas.groupby("p1")[["score1", "tempo_s"]].apply(lambda x: x.sum())
    score1_tempo = score1_tempo.reset_index()
    rank_ST = jogadores.merge(score1_tempo, left_on = jogadores.index, right_on="p1").drop(columns = ["id"])

    return rank_ST[["nome", "mmr", "p1", "score1", "tempo_s"]]



def tabelas(request, tabela1 = tabela1, tabela2 = tabela2):
    tabela1 = tabela1().head(10)
    tabela2 = tabela2().head(20)

    mydict = {"score1_tempo": tabela1.to_html(col_space=150,justify='center'),
            "rank_ST": tabela2.to_html(col_space=150,justify='center')}

    return render(request,"kayo/analise_kayo.html", context=mydict)

# OBS: Os códigos abaixo são apenas para mostrar como os gráficos foram feitos
# Apenas a imagem png dos gráficos foi usada em nas páginas HTML
# Por questões de ao tentar invocar as funções as imagens 
# ficavam com as cores e as características astéticas erradas

def grafico1(tabela1 = tabela1):

    score1_tempo = tabela1()

    # Mudança de características estéticas no boxplot

    PROPS = {
        "boxprops":{"edgecolor":"white"},
        "medianprops":{"color":"white"},
        "whiskerprops":{"color":"white"},
        "capprops":{"color":"white"},
        "flierprops": {"markerfacecolor": "white", "markersize": 12, "marker": "o"},
        "meanprops": {"color": "white"},
        "medianprops": {"color": "white", "alpha": 0.5}

    }

    # Alterações estéticas na plotagem

    sns.set_theme(font_scale=2, style="whitegrid",
    rc={"figure.figsize":(6, 10),
        "axes.facecolor": "#1f1f1f",
        "figure.facecolor": "#1f1f1f",
        "text.color": "white",
        "axes.labelcolor": "white",
        "xtick.color": "white",
        "ytick.color": "white"})

    # Definição do gráfico e sua plotagem

    figura1 = sns.boxplot(data=score1_tempo, y="tempo", color = "purple", **PROPS)
    figura1.axhline(sum(score1_tempo["tempo"])/len(score1_tempo["tempo"]), color = "white", linestyle = "--")
    figura1.set(ylabel="Tempo (min)")
    figura1.set_title("Tempo médio gasto na plataforma")
    figura1.grid(alpha = 0.2, axis="y")
    figura1.annotate("34", (-0.6, 32), annotation_clip=False)
    plt.text(-0.7,-12,"OBS: 34 minutos representa a média total")

    return plt.show()



def grafico2(tabela2 = tabela2):

    rank_ST = tabela2()

    # Criação de variáveis para dataframe de análise final

    categoria_0_20 = rank_ST.sort_values("rank")
    categoria_0_20 = categoria_0_20.loc[rank_ST["rank"] <= 20].reset_index(drop=True)
    tempo_medio_0_20 = categoria_0_20["tempo"].sum()/(len(categoria_0_20.index))

    categoria_21_40 = rank_ST.sort_values("rank")
    categoria_21_40 = categoria_21_40.loc[(rank_ST["rank"] <= 40) & (rank_ST["rank"] >= 21)].reset_index(drop=True)
    tempo_medio_21_40 = categoria_21_40["tempo"].sum()/(len(categoria_21_40.index))

    categoria_41_60 = rank_ST.sort_values("rank")
    categoria_41_60 = categoria_41_60.loc[(rank_ST["rank"] <= 60) & (rank_ST["rank"] >= 41)].reset_index(drop=True)
    tempo_medio_41_60 = categoria_41_60["tempo"].sum()/(len(categoria_41_60.index))

    categoria_61_80 = rank_ST.sort_values("rank")
    categoria_61_80 = categoria_61_80.loc[(rank_ST["rank"] <= 80) & (rank_ST["rank"] >= 61)].reset_index(drop=True)
    tempo_medio_61_80 = categoria_61_80["tempo"].sum()/(len(categoria_61_80.index))

    categoria_81_100 = rank_ST.sort_values("rank")
    categoria_81_100 = categoria_81_100.loc[(rank_ST["rank"] <= 100) & (rank_ST["rank"] >= 81)].reset_index(drop=True)
    tempo_medio_81_100 = categoria_81_100["tempo"].sum()/(len(categoria_81_100.index))

    #Listas para criação do dataframe final

    categorias_rank = ["0~20", "21~40", "41~60", "61~80", "81~100"]
    tempos_rank = [tempo_medio_0_20, tempo_medio_21_40, tempo_medio_41_60, tempo_medio_61_80, tempo_medio_81_100]

    df = pd.DataFrame(list(zip(categorias_rank,tempos_rank)), columns = ["Categorias", "Tempo"])

    # Alterações estéticas na plotagem

    sns.set_theme(font_scale=2, style="whitegrid",
    rc={"figure.figsize": (8, 8),
        "axes.facecolor": "#1f1f1f",
        "figure.facecolor": "#1f1f1f",
        "text.color": "white",
        "axes.labelcolor": "white",
        "xtick.color": "white",
        "ytick.color": "white"})

    # Definição do gráfico e sua plotagem

    figura2 = sns.barplot(data = df, x="Categorias", y="Tempo", palette=sns.color_palette("cool", 5), edgecolor="black")
    figura2.axhline(sum(tempos_rank)/len(tempos_rank), color = "white", linestyle = "--")
    figura2.set(xlabel = "Categorias", ylabel="Tempo (min)")
    figura2.set_title("Tempo médio por rank")
    figura2.grid(alpha = 0.2, axis="y")
    figura2.annotate("34", (4.6, 33.3), annotation_clip=False)
    plt.text(-0.52,-8,"OBS: 34 minutos representa a média total")
    return plt.show()



def grafico3(tabela2 = tabela2):

    rank_ST = tabela2()

    # Criação de variáveis para dataframe de análise final

    categoria_10_17 = rank_ST.sort_values("idade")
    categoria_10_17 = categoria_10_17.loc[rank_ST["idade"] <= 17].reset_index(drop=True)
    tempo_medio_10_17 = categoria_10_17["tempo"].sum()/(len(categoria_10_17.index))

    categoria_18_26 = rank_ST.sort_values("idade")
    categoria_18_26 = categoria_18_26.loc[(rank_ST["idade"] <= 26) & (rank_ST["idade"] >= 18)].reset_index(drop=True)
    tempo_medio_18_26 = categoria_18_26["tempo"].sum()/(len(categoria_18_26.index))

    categoria_27_35 = rank_ST.sort_values("idade")
    categoria_27_35 = categoria_27_35.loc[(rank_ST["idade"] <= 35) & (rank_ST["idade"] >= 27)].reset_index(drop=True)
    tempo_medio_27_35 = categoria_27_35["tempo"].sum()/(len(categoria_27_35.index))

    #Listas para criação do dataframe final

    categorias_idade = ["10~17", "18~26", "27~35"]
    tempos_idade = [tempo_medio_10_17, tempo_medio_18_26, tempo_medio_27_35]

    df_2 = pd.DataFrame(list(zip(categorias_idade,tempos_idade)), columns = ["Idades", "Tempo"])

    # Alterações estéticas na plotagem

    sns.set_theme(font_scale=2, style="whitegrid",
    rc={"figure.figsize": (8, 10),
        "axes.facecolor": "#1f1f1f",
        "figure.facecolor": "#1f1f1f",
        "text.color": "white",
        "axes.labelcolor": "white",
        "xtick.color": "white",
        "ytick.color": "white"})

    # Definição do gráfico e sua plotagem

    figura3 = sns.barplot(data = df_2, x="Idades", y="Tempo", palette=sns.color_palette("Blues", 3), edgecolor="black")
    figura3.axhline(sum(tempos_idade)/len(tempos_idade),  color = "white", linestyle = "--")
    figura3.set(xlabel = "Idades", ylabel="Tempo (min)")
    figura3.set_title("Tempo médio por idade")
    figura3.grid(alpha = 0.2, axis="y")
    figura3.annotate("34", (2.57, 33.5), annotation_clip=False)
    plt.text(-0.52,-6,"OBS: 34 minutos representa a média total")
# Alterações estéticas na plotagem

    sns.set_theme(font_scale=2, style="whitegrid",
    rc={"figure.figsize": (8, 10),
        "axes.facecolor": "#1f1f1f",
        "figure.facecolor": "#1f1f1f",
        "text.color": "white",
        "axes.labelcolor": "white",
        "xtick.color": "white",
        "ytick.color": "white"})

    # Definição do gráfico e sua plotagem

    figura3 = sns.barplot(data = df_2, x="Idades", y="Tempo", palette=sns.color_palette("Blues", 3), edgecolor="black")
    figura3.axhline(sum(tempos_idade)/len(tempos_idade),  color = "white", linestyle = "--")
    figura3.set(xlabel = "Idades", ylabel="Tempo (min)")
    figura3.set_title("Tempo médio por idade")
    figura3.grid(alpha = 0.2, axis="y")
    figura3.annotate("34", (2.57, 33.5), annotation_clip=False)
    plt.text(-0.52,-6,"OBS: 34 minutos representa a média total")
    return plt.show()