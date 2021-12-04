from django.db.models.fields import EmailField
from django.shortcuts import render, reverse
from django.http import HttpResponse, Http404
from django.http.response import HttpResponseRedirect
import pandas as pd
from menu.models import Jogador, Partida
from django.db.models import Q #permitir o OU na busca no banco

logged=False

# Create your views here.
def index(request):
    global logged
    return render(request,"menu/index.html",context={"logged":str(logged)})

def modos(request):
    return render(request,"menu/modos.html")

def leaderboards(request):
    
    item = Jogador.objects.all().values()
    jogadores = pd.DataFrame(item)

    item2 = Partida.objects.all().values()
    partidas = pd.DataFrame(item2)

    por_jogador = partidas.groupby('p1').mean().round(2)

    jogadores['media_pontos'] = jogadores.index.map(por_jogador['score1'])

    leaderboard = jogadores.sort_values(['mmr','media_pontos'], ascending=False)

    colunas = ['nome', 'mmr', 'media_pontos']
    context = {
        'leaderboard': leaderboard.reset_index()[colunas].to_html(col_space=70,justify='center')
    }

    return render(request,"menu/leaderboard.html", context)

def login(request):
    global logged
    if(logged):
        url = reverse("profile")
        return HttpResponseRedirect(url)
    if(request.POST):
        print("ok")
        lembrar = request.POST["remember"]=="lembrar"
        if lembrar:
            print("lembrando")
        try:
            user = Jogador.objects.get(Q(nome=request.POST["inputUser"]) | Q(email=request.POST["inputUser"]))
        except: 
            user = False
        if user:
            if user.hash_senha == request.POST["inputPassword"]:
                logged = user
                url = reverse("index")
                return HttpResponseRedirect(url)
            else:
                print("senha errada")
        else:
            print("Usuario não existente")

    lista_usuarios = Jogador.objects.all().values()
    lista_usuarios = pd.DataFrame(lista_usuarios)[["nome","hash_senha"]].rename(columns={"hash_senha":"senha"})
    lista_usuarios = lista_usuarios.to_html(col_space=70,justify='center')
    mydict={"usuarios":lista_usuarios}
    return render(request,"menu/login.html",context=mydict)
    
def modos_explicacao(request):
    return render(request,"menu/modos_explicacao.html")

def profile(request):
    global logged
    if(logged):
        user = logged
        db_values = Jogador.objects.all().values()
        df_players = pd.DataFrame(db_values)
        df_players = df_players[["nome","mmr","idade","email"]]

        db_values  = Partida.objects.all().values()
        df_matches = pd.DataFrame(db_values)
        df_matches = df_matches[["p1","p2","score1","score2","tempo_s"]].rename(columns={"tempo_s":"tempo"})

        df_matches,df_players = add_match_columns(df_matches,df_players)
        partidas_jogadas = df_players[df_players["nome"]==user.nome]["partidas-jogadas"]
        partidas_jogadas = int(partidas_jogadas)
        vitorias = df_players[df_players["nome"]==user.nome]["vitorias"]
        vitorias = int(vitorias)
        tempo_de_jogo = df_players[df_players["nome"]==user.nome]["tempo-jogo"]
        tempo_de_jogo = round(float(tempo_de_jogo)/60,2)
        # tempo_de_jogo = int(tempo_de_jogo)

        mmr = df_players[df_players["nome"]==user.nome]["mmr"].copy()
        mmr = int(mmr)
        player_rank, rank_img = process_rank(mmr)
        rank_img = r"img/ranks/"+rank_img
        
        
        mydict = {
            "nome": user.nome,
            "partidas": partidas_jogadas,
            "vitorias": vitorias,
            "tempo_jogo": tempo_de_jogo,
            "player_rank": player_rank,
            "rank_img": rank_img
        }
        return render(request,"menu/profile.html", context=mydict)
    else:
        url = reverse("login")
        return HttpResponseRedirect(url)
    
def analises_menu(request):
    return render(request, "menu/analises_menu.html")

def notas(request):
    return render(request, "menu/notas.html")

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

def add_match_columns(df_matches,df_players):
    
    df_players["vitorias"] = 0
    df_players["partidas-jogadas"] = 0
    df_players["tempo-jogo"] = 0
    for i in range(df_matches.shape[0]):
        linha = df_matches.iloc[i]

        p1 = linha["p1"].copy()
        p2 = linha["p2"].copy()
        if linha["score1"]>linha["score2"]:
            n = df_players.loc[p1,"vitorias"].copy() + 1
            df_players.loc[p1,"vitorias"] = n
        elif linha["score2"]>linha["score1"]:
            n = df_players.loc[p2,"vitorias"].copy() + 1
            df_players.loc[p2,"vitorias"] = n

        n = df_players.loc[p1,"partidas-jogadas"].copy() + 1
        df_players.loc[p1,"partidas-jogadas"] = n
        t = df_players.loc[p1,"tempo-jogo"].copy() + linha["tempo"].copy()
        df_players.loc[p1,"tempo-jogo"] = t

        n = df_players.loc[p2,"partidas-jogadas"].copy() + 1
        df_players.loc[p2,"partidas-jogadas"] = n
        t = df_players.loc[p2,"tempo-jogo"].copy() + linha["tempo"].copy()
        df_players.loc[p2,"tempo-jogo"] = t

    return df_matches,df_players

def process_rank(mmr):
    rank_dict = { # min, max, img-icon
        "Bronze":   [0,30,"bronze.png"],
        "Prata":    [30,50,"silver.png"],
        "Ouro":     [50,70,"gold.png"],
        "Platina":  [70,85,"plat.png"],
        "Mestre":   [85,101,"master.png"]
    }
    for rank in rank_dict:
        att = rank_dict[rank]
        if (mmr>=att[0] and mmr<att[1]):
            player_rank = rank
    return player_rank, rank_dict[player_rank][2]