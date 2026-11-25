from django.db import models

from core.models import DaEquipe


class Membro(DaEquipe):
    nome = models.CharField(max_length=100)
    email = models.CharField(max_length=150)
    cargo = models.CharField(max_length=50)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome


class Projeto(DaEquipe):
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    data_inicio = models.DateField()
    concluido = models.BooleanField(default=False)

    def __str__(self):
        return self.nome


class Subtarefa(DaEquipe):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    projeto = models.ForeignKey(
        Projeto,
        on_delete=models.PROTECT,
        related_name='subtarefas',
    )
    responsavel = models.ForeignKey(
        Membro,
        on_delete=models.PROTECT,
        related_name='responsabilidades',
    )
    prazo = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('a fazer', 'a fazer'),
            ('fazendo', 'fazendo'),
            ('feito', 'feito'),
        ],
        default='a fazer',
    )

    def __str__(self):
        return self.titulo

    def clean(self):
        from .regras import validar_subtarefa
        validar_subtarefa(self)


class Dependencia(DaEquipe):
    subtarefa = models.ForeignKey(
        Subtarefa,
        on_delete=models.PROTECT,
        related_name='dependencias',
    )
    subtarefa_dependente = models.ForeignKey(
        Subtarefa,
        on_delete=models.PROTECT,
        related_name='bloqueia',
    )
    obrigatoria = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.subtarefa} depende de {self.subtarefa_dependente}'

    def clean(self):
        from .regras import validar_dependencia
        validar_dependencia(self)
