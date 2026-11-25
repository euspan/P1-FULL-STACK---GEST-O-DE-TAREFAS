from django.db import migrations


def equipe_padrao(apps, schema_editor):
    Equipe = apps.get_model('core', 'Equipe')
    equipe, _ = Equipe.objects.get_or_create(nome='Equipe padrão')
    for nome in ('Membro', 'Projeto', 'Subtarefa', 'Dependencia'):
        Model = apps.get_model('tarefas', nome)
        Model.objects.filter(equipe__isnull=True).update(equipe=equipe)


class Migration(migrations.Migration):

    dependencies = [
        ('tarefas', '0004_equipe_nula'),
    ]

    operations = [
        migrations.RunPython(equipe_padrao, migrations.RunPython.noop),
    ]
