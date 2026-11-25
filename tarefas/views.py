from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

from .models import Dependencia, Membro, Projeto, Subtarefa


def equipe_atual(request):
    try:
        return request.user.perfil.equipe
    except ObjectDoesNotExist:
        return None


def _resposta_sem_equipe():
    return HttpResponse(
        'Seu usuário ainda não tem equipe. '
        'Cadastre um Perfil no Admin, ligando o usuário a uma equipe.'
    )


@login_required
def inicio(request):
    equipe = equipe_atual(request)
    if equipe is None:
        return _resposta_sem_equipe()

    projetos = Projeto.objects.filter(equipe=equipe)
    membros = Membro.objects.filter(equipe=equipe)
    subtarefas = Subtarefa.objects.filter(equipe=equipe)
    dependencias = Dependencia.objects.filter(equipe=equipe)

    html = f'<h1>Gestor de Tarefas — {equipe}</h1>'
    html += '<p><a href="/progresso/">Progresso</a></p>'

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


@login_required
def listar_projetos(request):
    equipe = equipe_atual(request)
    if equipe is None:
        return _resposta_sem_equipe()
    projetos = Projeto.objects.filter(equipe=equipe)
    texto = ', '.join(str(p) for p in projetos)
    return HttpResponse(f'Projetos: {texto}')


@login_required
def listar_pendentes(request):
    equipe = equipe_atual(request)
    if equipe is None:
        return _resposta_sem_equipe()
    base = Subtarefa.objects.filter(equipe=equipe)
    a_fazer = base.filter(status='a fazer')
    fazendo = base.filter(status='fazendo')
    pendentes = list(a_fazer) + list(fazendo)
    texto = ', '.join(str(s) for s in pendentes)
    return HttpResponse(f'Pendentes: {texto}')


@login_required
def buscar_tarefa(request):
    equipe = equipe_atual(request)
    if equipe is None:
        return _resposta_sem_equipe()
    titulo_busca = request.GET.get('titulo', '')
    resultados = Subtarefa.objects.filter(
        equipe=equipe,
        titulo__icontains=titulo_busca,
    )
    texto = ', '.join(str(s) for s in resultados)
    return HttpResponse(f'Resultado da busca: {texto}')


@login_required
def filtrar_status(request):
    equipe = equipe_atual(request)
    if equipe is None:
        return _resposta_sem_equipe()
    status_busca = request.GET.get('status', 'a fazer')
    resultados = Subtarefa.objects.filter(equipe=equipe, status=status_busca)
    texto = ', '.join(str(s) for s in resultados)
    return HttpResponse(f'Subtarefas "{status_busca}": {texto}')
