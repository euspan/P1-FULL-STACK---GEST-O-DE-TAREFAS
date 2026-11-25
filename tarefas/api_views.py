from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics

from .models import Dependencia, Membro, Projeto, Subtarefa
from .serializers import (
    DependenciaSerializer,
    MembroSerializer,
    ProjetoSerializer,
    SubtarefaSerializer,
)


class IsoladoPorEquipe:
    def get_queryset(self):
        try:
            equipe = self.request.user.perfil.equipe
        except ObjectDoesNotExist:
            return self.queryset.none()
        return self.queryset.filter(equipe=equipe)

    def perform_create(self, serializer):
        serializer.save(equipe=self.request.user.perfil.equipe)


class ProjetoListCreate(IsoladoPorEquipe, generics.ListCreateAPIView):
    queryset = Projeto.objects.all()
    serializer_class = ProjetoSerializer


class ProjetoDetail(IsoladoPorEquipe, generics.RetrieveUpdateDestroyAPIView):
    queryset = Projeto.objects.all()
    serializer_class = ProjetoSerializer


class MembroListCreate(IsoladoPorEquipe, generics.ListCreateAPIView):
    queryset = Membro.objects.all()
    serializer_class = MembroSerializer


class MembroDetail(IsoladoPorEquipe, generics.RetrieveUpdateDestroyAPIView):
    queryset = Membro.objects.all()
    serializer_class = MembroSerializer


class SubtarefaListCreate(IsoladoPorEquipe, generics.ListCreateAPIView):
    queryset = Subtarefa.objects.all()
    serializer_class = SubtarefaSerializer


class SubtarefaDetail(IsoladoPorEquipe, generics.RetrieveUpdateDestroyAPIView):
    queryset = Subtarefa.objects.all()
    serializer_class = SubtarefaSerializer


class DependenciaListCreate(IsoladoPorEquipe, generics.ListCreateAPIView):
    queryset = Dependencia.objects.all()
    serializer_class = DependenciaSerializer


class DependenciaDetail(IsoladoPorEquipe, generics.RetrieveUpdateDestroyAPIView):
    queryset = Dependencia.objects.all()
    serializer_class = DependenciaSerializer
