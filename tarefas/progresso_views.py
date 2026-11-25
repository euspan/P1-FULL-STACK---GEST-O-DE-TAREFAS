import csv

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from .dashboard import (
    base_da_equipe,
    progresso_por_projeto,
    ranking_responsaveis,
    resumo_progresso,
    serie_por_mes,
)
from .forms import PeriodoForm, filtrar_periodo
from .permissoes import papel_requerido
from .views import _resposta_sem_equipe, equipe_atual


def _base(request, equipe):
    return filtrar_periodo(request, base_da_equipe(equipe))


@login_required
def progresso(request):
    equipe = equipe_atual(request)
    if equipe is None:
        return _resposta_sem_equipe()
    qs = _base(request, equipe)
    eh_admin = request.user.perfil.eh_admin
    contexto = {
        'equipe': equipe,
        'kpis': resumo_progresso(qs),
        'projetos': progresso_por_projeto(equipe, qs),
        'ranking': ranking_responsaveis(qs),
        'por_mes': serie_por_mes(qs) if eh_admin else [],
        'mostra_series': eh_admin,
        'form': PeriodoForm(request.GET),
    }
    return render(request, 'tarefas/progresso.html', contexto)


def _celula(valor):
    texto = '' if valor is None else str(valor)
    if texto[:1] in '=+-@':
        return "'" + texto
    return texto


@papel_requerido('admin')
def exportar_csv(request):
    equipe = equipe_atual(request)
    if equipe is None:
        return _resposta_sem_equipe()
    qs = _base(request, equipe).select_related('projeto', 'responsavel')
    resposta = HttpResponse(content_type='text/csv')
    resposta['Content-Disposition'] = 'attachment; filename="subtarefas.csv"'
    escritor = csv.writer(resposta)
    escritor.writerow(['Projeto', 'Título', 'Responsável', 'Status', 'Prazo'])
    for subtarefa in qs:
        escritor.writerow([
            _celula(subtarefa.projeto.nome),
            _celula(subtarefa.titulo),
            _celula(subtarefa.responsavel.nome),
            subtarefa.status,
            subtarefa.prazo,
        ])
    return resposta
