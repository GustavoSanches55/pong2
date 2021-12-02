import random

jogadores = []
variacao_skill = 10 # Margem de erro da habilidade de cada jogador
duracao_partida = 5
limite_pontos = 10

def sim_partida(jogador1, jogador2):
    p1 = jogador1["skill"] * (1+random.randint( -variacao_skill, variacao_skill)/100)
    p2 = jogador2["skill"] * (1+random.randint( -variacao_skill, variacao_skill)/100)
    print(p1-p2) # Diferença de habilidade entre eles, numero negativo = Jogador 2 é melhor

