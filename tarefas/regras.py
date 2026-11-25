from django.core.exceptions import ObjectDoesNotExist, ValidationError


def validar_subtarefa(subtarefa):
    erros = []
    if subtarefa.projeto_id and subtarefa.equipe_id:
        try:
            if subtarefa.projeto.equipe_id != subtarefa.equipe_id:
                erros.append('O projeto precisa ser da mesma equipe.')
        except ObjectDoesNotExist:
            erros.append('O projeto informado não existe.')
    if subtarefa.responsavel_id and subtarefa.equipe_id:
        try:
            if subtarefa.responsavel.equipe_id != subtarefa.equipe_id:
                erros.append('O responsável precisa ser da mesma equipe.')
        except ObjectDoesNotExist:
            erros.append('O responsável informado não existe.')
    if subtarefa.status == 'feito' and subtarefa.pk:
        from .models import Dependencia
        abertas = Dependencia.objects.filter(
            subtarefa_id=subtarefa.pk,
            obrigatoria=True,
        ).exclude(subtarefa_dependente__status='feito')
        if abertas.exists():
            erros.append(
                'Não é possível concluir enquanto a dependência obrigatória estiver aberta.'
            )
    if erros:
        raise ValidationError(erros)


def validar_dependencia(dependencia):
    erros = []
    if not (dependencia.subtarefa_id and dependencia.subtarefa_dependente_id):
        if erros:
            raise ValidationError(erros)
        return
    if dependencia.subtarefa_id == dependencia.subtarefa_dependente_id:
        erros.append('Uma subtarefa não pode depender de si mesma.')
    else:
        try:
            if dependencia.subtarefa.equipe_id != dependencia.subtarefa_dependente.equipe_id:
                erros.append('A dependência precisa ligar subtarefas da mesma equipe.')
        except ObjectDoesNotExist:
            erros.append('A subtarefa informada não existe.')
    if dependencia.equipe_id and dependencia.subtarefa_id:
        try:
            if dependencia.subtarefa.equipe_id != dependencia.equipe_id:
                erros.append('A dependência precisa ser da mesma equipe da subtarefa.')
        except ObjectDoesNotExist:
            erros.append('A subtarefa informada não existe.')
    if erros:
        raise ValidationError(erros)
