import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tarefas', '0005_equipe_padrao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membro',
            name='equipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.equipe'),
        ),
        migrations.AlterField(
            model_name='projeto',
            name='equipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.equipe'),
        ),
        migrations.AlterField(
            model_name='subtarefa',
            name='equipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.equipe'),
        ),
        migrations.AlterField(
            model_name='dependencia',
            name='equipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.equipe'),
        ),
    ]
