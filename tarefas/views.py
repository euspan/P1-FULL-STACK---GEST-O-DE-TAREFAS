from django.http import HttpResponse


def inicio(request):
    return HttpResponse('Olá, gestor de tarefas!')
def buscar_tarefa(request):
    titulo_busca = request.GET.get('titulo', '')
    resultados = Subtarefa.objects.filter(titulo__icontains=titulo_busca)
    texto = ', '.join(str(s) for s in resultados)
    return HttpResponse(f'Resultado da busca: {texto}')
