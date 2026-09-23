from django.http import HttpResponse


def inicio(request):
    return HttpResponse('Olá, gestor de tarefas!')

def buscar_tarefa(request):
    titulo_busca = request.GET.get('titulo', '')
    resultados = Subtarefa.objects.filter(titulo__icontains=titulo_busca)
    texto = ', '.join(str(s) for s in resultados)
    return HttpResponse(f'Resultado da busca: {texto}')

def filtrar_status(request):
    status_busca = request.GET.get('status', 'a fazer')
    resultados = Subtarefa.objects.filter(status=status_busca)
    texto = ', '.join(str(s) for s in resultados)
    return HttpResponse(f'Subtarefas "{status_busca}": {texto}')