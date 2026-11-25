from django.urls import path

from .api_views import (
    DependenciaDetail,
    DependenciaListCreate,
    MembroDetail,
    MembroListCreate,
    ProjetoDetail,
    ProjetoListCreate,
    SubtarefaDetail,
    SubtarefaListCreate,
)

urlpatterns = [
    path('projetos/', ProjetoListCreate.as_view()),
    path('projetos/<int:pk>/', ProjetoDetail.as_view()),
    path('membros/', MembroListCreate.as_view()),
    path('membros/<int:pk>/', MembroDetail.as_view()),
    path('subtarefas/', SubtarefaListCreate.as_view()),
    path('subtarefas/<int:pk>/', SubtarefaDetail.as_view()),
    path('dependencias/', DependenciaListCreate.as_view()),
    path('dependencias/<int:pk>/', DependenciaDetail.as_view()),
]
