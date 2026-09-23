from django.urls import path
from .. import views

urlpatterns = [
    path('', views.inicio),
    path('buscar/', views.buscar_tarefa),
    path('status/', views.filtrar_status),
]

