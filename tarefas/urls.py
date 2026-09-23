from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio),
    path('projetos/', views.listar_projetos),
    path('pendentes/', views.listar_pendentes),
    path('buscar/', views.buscar_tarefa),
    path('status/', views.filtrar_status),
]
