from django.urls import path

from . import progresso_views, views

urlpatterns = [
    path('', views.inicio),
    path('projetos/', views.listar_projetos),
    path('pendentes/', views.listar_pendentes),
    path('buscar/', views.buscar_tarefa),
    path('status/', views.filtrar_status),
    path('progresso/', progresso_views.progresso, name='progresso'),
]