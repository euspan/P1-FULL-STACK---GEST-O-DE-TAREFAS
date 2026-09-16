from django.db import models


class Membro(models.Model):
    nome = models.CharField(max_length=100)
    email = models.CharField(max_length=150)
    cargo = models.CharField(max_length=50)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome


class Projeto(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    data_inicio = models.DateField()
    concluido = models.BooleanField(default=False)

    def __str__(self):
        return self.nome


class Subtarefa(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    # relaciona com Projeto e Membro guardando o id,
    # já que ForeignKey não foi visto na Aula 4
    projeto_id = models.IntegerField()
    responsavel_id = models.IntegerField()
    prazo = models.DateField()
    concluida = models.BooleanField(default=False)

    def __str__(self):
        return self.titulo


class Dependencia(models.Model):
    # subtarefa que possui a dependência
    subtarefa_id = models.IntegerField()
    # subtarefa que precisa ser concluída antes
    subtarefa_dependente_id = models.IntegerField()
    obrigatoria = models.BooleanField(default=True)

    def __str__(self):
        return f"Subtarefa {self.subtarefa_id} depende de {self.subtarefa_dependente_id}"
