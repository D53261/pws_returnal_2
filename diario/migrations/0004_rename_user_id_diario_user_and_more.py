# Generated by Django 5.1.4 on 2025-01-09 17:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diario', '0003_usuario_diario_user_id_pessoa_user_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='diario',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='pessoa',
            old_name='user_id',
            new_name='user',
        ),
    ]