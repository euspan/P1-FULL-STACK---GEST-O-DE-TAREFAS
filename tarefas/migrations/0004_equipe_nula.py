import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('tarefas', '0003_remove_subtarefa_concluida_alter_subtarefa_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='membro',
            name='equipe',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='core.equipe'),
        ),
        migrations.AddField(
            model_name='projeto',
            name='equipe',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='core.equipe'),
        ),
        migrations.AddField(
            model_name='subtarefa',
            name='equipe',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='core.equipe'),
        ),
        migrations.AddField(
            model_name='dependencia',
            name='equipe',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='core.equipe'),
        ),
    ]
