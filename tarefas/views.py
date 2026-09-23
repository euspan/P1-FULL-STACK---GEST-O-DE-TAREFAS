from django.http import HttpResponse
from .models import Projeto, Subtarefa, Dependencia, Membro


def inicio(request):
    projetos = Projeto.objects.all()
    membros = Membro.objects.all()
    subtarefas = Subtarefa.objects.all()
    dependencias = Dependencia.objects.all()

    html = '<h1>Gestor de Tarefas</h1>'

    html += '<h2>Projetos</h2><ul>'
    for p in projetos:
        html += f'<li>{p}</li>'
    html += '</ul>'

    html += '<h2>Membros</h2><ul>'
    for m in membros:
        html += f'<li>{m}</li>'
    html += '</ul>'

    html += '<h2>Subtarefas</h2><ul>'
    for s in subtarefas:
        html += f'<li>{s} — status: {s.status}</li>'
    html += '</ul>'

    html += '<h2>Dependências</h2><ul>'
    for d in dependencias:
        html += f'<li>{d}</li>'
    html += '</ul>'

    return HttpResponse(html)


def listar_projetos(request):
    projetos = Projeto.objects.all()
    texto = ', '.join(str(p) for p in projetos)
    return HttpResponse(f'Projetos: {texto}')


def listar_pendentes(request):
    pendentes = Subtarefa.objects.filter(concluida=False)
    texto = ', '.join(str(s) for s in pendentes)
    return HttpResponse(f'Pendentes: {texto}')


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