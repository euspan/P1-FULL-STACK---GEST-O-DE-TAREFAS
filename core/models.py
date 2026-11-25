from django.contrib.auth.models import User
from django.db import models


class Equipe(models.Model):
    nome = models.CharField(max_length=120)
    criada_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


class DaEquipe(models.Model):
    equipe = models.ForeignKey(
        'core.Equipe',
        on_delete=models.PROTECT,
    )

    class Meta:
        abstract = True


class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    equipe = models.ForeignKey(Equipe, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.usuario.username} ({self.equipe})'
