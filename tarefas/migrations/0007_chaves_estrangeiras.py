import django.db.models.deletion
from django.db import migrations, models


def limpar_orfaos(apps, schema_editor):
    Projeto = apps.get_model('tarefas', 'Projeto')
    Membro = apps.get_model('tarefas', 'Membro')
    Subtarefa = apps.get_model('tarefas', 'Subtarefa')
    Dependencia = apps.get_model('tarefas', 'Dependencia')
    projetos = set(Projeto.objects.values_list('id', flat=True))
    membros = set(Membro.objects.values_list('id', flat=True))
    invalidas = [
        subtarefa.pk
        for subtarefa in Subtarefa.objects.all()
        if subtarefa.projeto_id not in projetos or subtarefa.responsavel_id not in membros
    ]
    if invalidas:
        Dependencia.objects.filter(subtarefa_id__in=invalidas).delete()
        Dependencia.objects.filter(subtarefa_dependente_id__in=invalidas).delete()
        Subtarefa.objects.filter(pk__in=invalidas).delete()
    subtarefas = set(Subtarefa.objects.values_list('id', flat=True))
    for dependencia in Dependencia.objects.all():
        if (
            dependencia.subtarefa_id not in subtarefas
            or dependencia.subtarefa_dependente_id not in subtarefas
        ):
            dependencia.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('tarefas', '0006_equipe_obrigatoria'),
    ]

    operations = [
        migrations.RunPython(limpar_orfaos, migrations.RunPython.noop),
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.RemoveField(model_name='subtarefa', name='projeto_id'),
                migrations.AddField(
                    model_name='subtarefa',
                    name='projeto',
                    field=models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='subtarefas',
                        to='tarefas.projeto',
                    ),
                ),
                migrations.RemoveField(model_name='subtarefa', name='responsavel_id'),
                migrations.AddField(
                    model_name='subtarefa',
                    name='responsavel',
                    field=models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='responsabilidades',
                        to='tarefas.membro',
                    ),
                ),
                migrations.RemoveField(model_name='dependencia', name='subtarefa_id'),
                migrations.AddField(
                    model_name='dependencia',
                    name='subtarefa',
                    field=models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='dependencias',
                        to='tarefas.subtarefa',
                    ),
                ),
                migrations.RemoveField(model_name='dependencia', name='subtarefa_dependente_id'),
                migrations.AddField(
                    model_name='dependencia',
                    name='subtarefa_dependente',
                    field=models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='bloqueia',
                        to='tarefas.subtarefa',
                    ),
                ),
            ],
            database_operations=[],
        ),
    ]
