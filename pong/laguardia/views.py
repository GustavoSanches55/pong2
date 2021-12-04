from django.shortcuts import render_to_response



def index(request):
    


    mydict = {
        "partidas": partidas.head(10).to_html(col_space=70,justify='center'),
        "descricao": descricao.to_html(col_space=70,justify='center'),
        "por_jogador": por_jogador.head(10).to_html(col_space=70,justify='center')
    }
    return render(request,"sanches/index.html", context=mydict)

def analise():
    players = pd.DataFrame( Jogador.objects.all().values() )
    matches = pd.DataFrame( Partida.objects.all().values() )

    players = players.rename(columns={"","index"})

    matches = pd.merge(matches, players, left_on="p1", right_on="index")

    matplotlib.style.use('dark_background')

    graf1 = grafico1(players)
    graf2 = grafico2(matches)
    graf3 = grafico3(matches)
    graf4 = grafico4(players, matches)

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