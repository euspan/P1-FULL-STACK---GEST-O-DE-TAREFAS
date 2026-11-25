from django.db import migrations, models


def perfis_existentes_viram_admin(apps, schema_editor):
    Perfil = apps.get_model('core', 'Perfil')
    Perfil.objects.update(papel='admin')


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='papel',
            field=models.CharField(
                choices=[('admin', 'Administrador'), ('operador', 'Operador')],
                default='operador',
                max_length=20,
            ),
        ),
        migrations.RunPython(perfis_existentes_viram_admin, migrations.RunPython.noop),
    ]
