# Generated by Django 4.1 on 2022-08-28 10:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_rename_fechacreacion_plan_creationdate'),
    ]

    operations = [
        migrations.RenameField(
            model_name='plan',
            old_name='HoraCreacion',
            new_name='CreationTime',
        ),
    ]
