from django.db.models import Count, Q

from .models import Projeto, Subtarefa


def resumo_progresso(equipe):
    kpis = Subtarefa.objects.filter(equipe=equipe).aggregate(
        total=Count('id'),
        feitas=Count('id', filter=Q(status='feito')),
        fazendo=Count('id', filter=Q(status='fazendo')),
        a_fazer=Count('id', filter=Q(status='a fazer')),
    )
    total = kpis['total']
    feitas = kpis['feitas']
    kpis['percentual'] = round(100 * feitas / total) if total else 0
    return kpis


def progresso_por_projeto(equipe):
    stats = (
        Subtarefa.objects.filter(equipe=equipe)
        .values('projeto_id')
        .annotate(
            total=Count('id'),
            feitas=Count('id', filter=Q(status='feito')),
        )
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
