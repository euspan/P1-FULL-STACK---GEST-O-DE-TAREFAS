from django.urls import path
from .. import views

urlpatterns = [
    path('', views.inicio),
    path('buscar/', views.buscar_tarefa),
]

