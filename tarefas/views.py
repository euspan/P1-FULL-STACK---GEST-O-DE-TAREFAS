from django.http import HttpResponse


def inicio(request):
    return HttpResponse('Olá, gestor de tarefas!')
