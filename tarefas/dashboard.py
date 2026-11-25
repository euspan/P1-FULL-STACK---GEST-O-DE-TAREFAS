from django.db.models import Count, Q
from django.db.models.functions import TruncMonth

from .models import Projeto, Subtarefa


def resumo_progresso(qs):
    kpis = qs.aggregate(
        total=Count('id'),
        feitas=Count('id', filter=Q(status='feito')),
        fazendo=Count('id', filter=Q(status='fazendo')),
        a_fazer=Count('id', filter=Q(status='a fazer')),
    )
    total = kpis['total']
    feitas = kpis['feitas']
    kpis['percentual'] = round(100 * feitas / total) if total else 0
    return kpis


def progresso_por_projeto(equipe, qs):
    stats = qs.values('projeto_id').annotate(
        total=Count('id'),
        feitas=Count('id', filter=Q(status='feito')),
    )
    por_id = {linha['projeto_id']: linha for linha in stats}
    projetos = []
    for projeto in Projeto.objects.filter(equipe=equipe).order_by('nome'):
        linha = por_id.get(projeto.id)
        total = linha['total'] if linha else 0
        feitas = linha['feitas'] if linha else 0
        projetos.append({
            'projeto': projeto.nome,
            'total': total,
            'feitas': feitas,
            'percentual': round(100 * feitas / total) if total else 0,
        })
    return projetos


def ranking_responsaveis(qs):
    return (
        qs.values('responsavel__nome')
        .annotate(total=Count('id'))
        .order_by('-total')[:5]
    )


def serie_por_mes(qs):
    linhas = (
        qs.annotate(mes=TruncMonth('prazo'))
        .values('mes')
        .annotate(total=Count('id'))
        .order_by('mes')
    )
    return [
        {
            'mes': linha['mes'].strftime('%m/%Y') if linha['mes'] else '',
            'total': linha['total'],
        }
        for linha in linhas
    ]


def base_da_equipe(equipe):
    return Subtarefa.objects.filter(equipe=equipe)
