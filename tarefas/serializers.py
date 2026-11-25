from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import serializers

from .models import Dependencia, Membro, Projeto, Subtarefa


def _equipe_da_requisicao(serializer):
    request = serializer.context.get('request')
    if request is None:
        return None
    try:
        return request.user.perfil.equipe
    except (AttributeError, ObjectDoesNotExist):
        return None


def _restringir(serializer, campos):
    equipe = _equipe_da_requisicao(serializer)
    if equipe is None:
        return
    for nome in campos:
        serializer.fields[nome].queryset = serializer.fields[nome].queryset.filter(equipe=equipe)


def _validar_modelo(serializer, data):
    instance = serializer.instance or serializer.Meta.model()
    equipe = _equipe_da_requisicao(serializer)
    if equipe is not None:
        instance.equipe = equipe
    for campo, valor in data.items():
        setattr(instance, campo, valor)
    try:
        instance.clean()
    except ValidationError as exc:
        if getattr(exc, 'message_dict', None):
            raise serializers.ValidationError(exc.message_dict)
        raise serializers.ValidationError(exc.messages)
    return data


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
            'id', 'titulo', 'descricao', 'projeto', 'responsavel',
            'prazo', 'status', 'equipe',
        ]
        read_only_fields = ['equipe']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _restringir(self, ['projeto', 'responsavel'])

    def validate(self, data):
        return _validar_modelo(self, data)


class DependenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dependencia
        fields = ['id', 'subtarefa', 'subtarefa_dependente', 'obrigatoria', 'equipe']
        read_only_fields = ['equipe']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _restringir(self, ['subtarefa', 'subtarefa_dependente'])

    def validate(self, data):
        return _validar_modelo(self, data)
