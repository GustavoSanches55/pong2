from django.db import models

# Create your models here.
class Partida(models.Model):
    p1 = models.IntegerField()
    p2 = models.IntegerField()
    score1 = models.IntegerField()
    score2 = models.IntegerField()
    tempo_s = models.IntegerField()

class Jogador(models.Model):
    nome = models.CharField(max_length=80)
    mmr = models.IntegerField()
    idade = models.IntegerField()
    email = models.CharField(max_length=80)
    hash_senha = models.CharField(max_length=15)