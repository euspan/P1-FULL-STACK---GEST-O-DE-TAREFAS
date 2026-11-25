from rest_framework import serializers

from .models import Dependencia, Membro, Projeto, Subtarefa


class ProjetoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projeto
        fields = ['id', 'nome', 'descricao', 'data_inicio', 'concluido', 'equipe']
        read_only_fields = ['equipe']


class MembroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membro
        fields = ['id', 'nome', 'email', 'cargo', 'ativo', 'equipe']
        read_only_fields = ['equipe']


class SubtarefaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtarefa
        fields = [
            'id', 'titulo', 'descricao', 'projeto_id', 'responsavel_id',
            'prazo', 'status', 'equipe',
        ]
        read_only_fields = ['equipe']


class DependenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dependencia
        fields = [
            'id', 'subtarefa_id', 'subtarefa_dependente_id',
            'obrigatoria', 'equipe',
        ]
        read_only_fields = ['equipe']
