from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .dashboard import progresso_por_projeto, resumo_progresso
from .views import _resposta_sem_equipe, equipe_atual


@login_required
def progresso(request):
    equipe = equipe_atual(request)
    if equipe is None:
        return _resposta_sem_equipe()
    contexto = {
        'equipe': equipe,
        'kpis': resumo_progresso(equipe),
        'projetos': progresso_por_projeto(equipe),
    }
    return render(request, 'tarefas/progresso.html', contexto)
